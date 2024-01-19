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
from typing import Optional

from ..embedding.embedding import Embedding
from ..embedding.openai_embedding import OpenAIEmbedding
from ..llm.llm import LLM
from ..llm.openai import OpenAI
from ..utils.functions import generate_random_str


class EngineConfig(ABC):
    @abstractmethod
    def get_application_id(self) -> Optional[str]:
        pass

    @abstractmethod
    def create_application_id(self) -> str:
        pass


class LocalEngineConfig(EngineConfig):
    """LocalEngineConfig is a configuration object for using Arcus
     Prompt Enrichment locally.

    Attributes:
        llm: The LLM to use for the engine.
        embedding: The embedding to use for the engine.
        application_id: The application ID to use for the engine.
    """

    def __init__(
        self,
        llm: LLM,
        embedding: Embedding,
        application_id: Optional[str] = None,
    ):
        self.llm = llm
        self.embedding = embedding
        self.application_id = application_id

    def get_llm(self) -> LLM:
        return self.llm

    def get_embedding(self) -> Embedding:
        return self.embedding

    def create_application_id(self) -> str:
        self.application_id = generate_random_str()
        return self.application_id

    def get_application_id(self) -> Optional[str]:
        return self.application_id


class ClientEngineConfig(EngineConfig):
    """ClientEngineConfig is a configuration object for using Arcus
     Prompt Enrichment as a client.

    Attributes:
        llm: The LLM to use for the engine.
        application_id: The application ID to use for the engine.
        call_llm_local (bool): Whether to call the LLM locally from the SDK. If
            false, the LLM call will happen through the Arcus platform.
    """

    def __init__(
        self,
        application_id: str,
        call_llm_local: bool = False,
        llm: Optional[LLM] = None,
    ):
        self.llm = llm
        self.application_id = application_id
        self.call_llm_local = call_llm_local

        if self.call_llm_local:
            assert (
                self.llm is not None
            ), "LLM must be provided when calling LLM from Client SDK."

    def get_llm(self) -> Optional[LLM]:
        return self.llm

    def get_call_llm_local(self) -> bool:
        return self.call_llm_local

    def get_application_id(self) -> str:
        return self.application_id

    def create_application_id(self) -> str:
        pass


def create_default_local_engine_config() -> LocalEngineConfig:
    """Create a default local engine configuration."""
    return LocalEngineConfig(
        llm=OpenAI(),
        embedding=OpenAIEmbedding(),
    )
