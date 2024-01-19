# Copyright [2024] [Arcus Inc.]

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from abc import ABC, abstractmethod
from collections.abc import Generator
from typing import List, Union

from arcus.client.client import ArcusResponse

from ..api_models.completion_models import (
    CompletionCall,
    CompletionCallResponse,
)
from ..api_models.query_models import QueryCall, QueryCallResponse
from ..dataset.dataset import Dataset
from ..engine.config import ClientEngineConfig, LocalEngineConfig
from ..indexing.index import Index
from ..llm.config import llm_to_config
from ..mode.mode import Mode
from ..prompt.prompt import Prompt, parse_prompt_to_message
from ..prompt.stuff_prompt_constructor import StuffPromptConstructor
from ..retriever.retriever import Retriever
from ..system.config import SystemConfig


class Engine(ABC):
    """The Engine is responsible for managing the indexing, retrieval,
    and text generation process of a Prompt Enrichment pipeline.
    """

    @abstractmethod
    def generate(
        self, prompt: str, stream: bool = False, **kwargs
    ) -> Union[str, Generator[str, None, None]]:
        """Generate text using the engine."""
        pass


class LocalEngine(Engine):
    def __init__(
        self,
        system_config: SystemConfig,
        config: LocalEngineConfig,
    ):
        self.system_config = system_config
        self.config = config
        assert (
            config.get_application_id() is not None
        ), "Application ID must be set for Engine."

        assert (
            self.system_config.get_mode() == Mode.LOCAL
        ), "Local Engine can only be created in local mode."

        self.index = Index(
            config.get_embedding(),
            self.system_config.get_vector_db_client(),
            config.get_application_id(),
        )
        self.retriever = Retriever(
            self.index,
        )
        self.llm = config.get_llm()
        self.prompt_constructor = StuffPromptConstructor()

    def update_index(self, datasets: List[Dataset]):
        """Updates the Engine's index with the given datasets."""
        for dataset in datasets:
            self.index.update(dataset)

    def generate(
        self, prompt: Prompt, stream: bool = False, **kwargs
    ) -> Union[str, Generator[str, None, None]]:
        """Generate text using the RAG engine."""
        messages = parse_prompt_to_message(prompt)

        nodes_context = self.retriever.query(messages)
        remaining_tokens = (
            self.llm.get_max_input_tokens()
            - self.llm.get_max_generation_tokens()
            - self.llm.get_overhead_tokens_per_response()
        )

        enriched_prompt = self.prompt_constructor.construct_prompt(
            nodes_context,
            messages,
            self.llm.get_tokenizer(),
            remaining_tokens,
            self.llm.get_overhead_tokens_per_message(),
        )

        return self.llm.generate(enriched_prompt, stream, **kwargs)


class ClientEngine(Engine):
    def __init__(
        self,
        system_config: SystemConfig,
        config: ClientEngineConfig,
    ):
        self.system_config = system_config
        self.config = config

        self.application_id = config.get_application_id()

        assert (
            self.application_id is not None
        ), "Application ID must be set for Engine."

        assert (
            self.system_config.get_mode() == Mode.MANAGED
        ), "Client Engine can only be created in managed mode."

        self.api_client = self.system_config.get_client()

        assert (
            self.api_client is not None
        ), "Client Engine requires an API client."

        self.call_llm_locally = self.config.get_call_llm_local()
        self.llm = None
        if self.call_llm_locally:
            self.llm = config.get_llm()

    def _query(self, query_call: QueryCall) -> QueryCallResponse:
        response: ArcusResponse = self.api_client.request(
            "POST",
            f"api/v1/applications/{self.application_id}/query",
            json=query_call.model_dump(),
            retryable=True,
        )

        if not response.status_ok:
            raise RuntimeError(
                "Failed to get additional context for query call: "
                + f"{query_call}. Response: {response.data}"
            )

        return QueryCallResponse(
            call_id=response.data["call_id"],
            enriched_prompt=response.data["enriched_prompt"],
        )

    def _complete(
        self, completion_call: CompletionCall
    ) -> CompletionCallResponse:
        response: ArcusResponse = self.api_client.request(
            "POST",
            f"api/v1/applications/{self.application_id}/completion",
            json=completion_call.model_dump(),
            retryable=True,
        )

        if not response.status_ok:
            raise RuntimeError(
                "Failed to generate response for completion: "
                + f"{completion_call}. Response: {response.data}"
            )

        return CompletionCallResponse(
            call_id=response.data["call_id"],
            response=response.data["response"],
        )

    def generate(
        self, prompt: Prompt, stream: bool = False, **kwargs
    ) -> Union[str, Generator[str, None, None]]:
        """Generate text using the RAG engine."""
        messages = parse_prompt_to_message(prompt)

        if self.call_llm_locally:
            query_call = QueryCall(
                prompt=messages,
                llm_config=llm_to_config(self.llm),
            )

            response = self._query(query_call)
            enriched_prompt = response.enriched_prompt

            return self.llm.generate(enriched_prompt, stream, **kwargs)

        completion_call = CompletionCall(prompt=messages)

        response = self._complete(completion_call)
        return response.response
