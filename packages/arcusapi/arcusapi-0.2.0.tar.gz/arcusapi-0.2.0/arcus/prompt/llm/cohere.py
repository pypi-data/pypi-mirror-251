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


import warnings
from collections.abc import Generator
from typing import Any, Dict, List, Optional, Tuple, Union

from cohere import CohereError

from ..llm.llm import LLM
from ..message.message import Message
from ..model_provider.cohere import (
    COHERE_TOKENIZERS,
    CohereModelType,
    create_cohere_client,
)
from ..model_provider.error import PromptModelError
from ..tokenizer.cohere_tokenizer import CohereTokenizer

STREAM_START = "stream-start"


class Cohere(LLM):
    """Access wrapper around a Cohere LLM model using their generate api.
    Details of the api can be seen at:
        https://docs.cohere.com/reference/generate.

    Attributes:
        model_type: The type of Cohere LLM to use. See CohereModelType
            for a list of supported options.
        temperature: The temperature to use for the LLM.
        max_tokens: The maximum number of tokens to generate.
        top_p: The top_p to use for the LLM.
        api_key (optional): The API key to use to access the Cohere API. If
            this is not provided, the COHERE_API_KEY environment variable
            will be used.
    """

    def __init__(
        self,
        model_type: CohereModelType = CohereModelType.COMMAND,
        temperature: float = 0.75,
        max_tokens: int = 256,
        top_p: float = 0.75,
        api_key: Optional[str] = None,
    ):
        super().__init__(model_type=model_type, max_gen_tokens=max_tokens)
        self.temperature = temperature
        self.top_p = top_p
        self.tokenizer = CohereTokenizer(COHERE_TOKENIZERS[self.model_type])

        try:
            self.cohere_client = create_cohere_client(api_key)
        except CohereError as e:
            warnings.warn(
                "Cohere API key not provided, unable to create "
                + "Cohere client. This means generating from "
                + f"this instance will be unavailable {e}"
            )
            self.cohere_client = None

    def get_config_dict(self) -> Dict[str, Any]:
        return {
            "max_tokens": self.max_gen_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p,
        }

    def generate(
        self, messages: List[Message], stream: bool = False, **kwargs
    ) -> Union[str, Generator[str, None, None]]:
        """Generate text based on a given input using the LLM."""
        message, history = self._construct_api_message_and_history(messages)

        try:
            # Note: Chat API is in beta and subject to change.
            response = self.cohere_client.chat(
                message=message,
                chat_history=history,
                model=self.model_type.value,
                temperature=self.temperature,
                max_tokens=self.max_gen_tokens,
                p=self.top_p,
                stream=stream,
                **kwargs,
            )
        except CohereError as err:
            raise PromptModelError(self.model_type, err)

        if stream:
            return self._construct_stream_generator(response)
        else:
            return response.text

    def _construct_stream_generator(
        self, response
    ) -> Generator[str, None, None]:
        for item in response:
            if item.event_type == STREAM_START:
                continue
            elif item.is_finished:
                break

            yield item.text

    def _construct_api_message_and_history(
        self, messages: List[Message]
    ) -> Tuple[str, List[Dict[str, str]]]:
        """Construct the prompt to use for the API call."""

        final_message = messages[-1].content
        history = []

        for message in messages[:-1]:
            if message.role == "user":
                history.append({"message": message.content, "role": "user"})
            elif message.role == "assistant":
                history.append({"message": message.content, "role": "chatbot"})
            elif message.role == "system":
                history.append({"message": message.content, "role": "system"})
            else:
                raise ValueError(
                    f"Message role {message.role} is not supported for "
                    + "Cohere LLM."
                )

        return final_message, history
