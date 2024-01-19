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
from typing import Any, Dict, List, Optional, Union

from openai import OpenAIError

from ..llm.llm import LLM
from ..message.message import Message
from ..model_provider.error import PromptModelError
from ..model_provider.openai import (
    OPENAI_TOKENIZERS,
    OpenAIModelType,
    create_openai_client,
)
from ..tokenizer.tiktoken_tokenizer import TiktokenTokenizer


class OpenAI(LLM):
    """OpenAI represents LLMs provided by OpenAI. For a full description of
    attributes, see https://platform.openai.com/docs/api-reference/chat/create.

    Attributes:
        model_type: The type of the OpenAI model to use.
        temperature: The temperature to use for the LLM.
        max_tokens: The maximum number of tokens to generate.
        top_p: The top_p to use for the LLM.
        frequency_penalty: The frequency penalty to use for the LLM.
        presence_penalty: The presence penalty to use for the LLM.
        api_key (optional): The API key to use to access the OpenAI API. If
            this is not provided, the OPENAI_API_KEY environment variable
            will be used.
    """

    def __init__(
        self,
        model_type: OpenAIModelType = OpenAIModelType.GPT_35_TURBO,
        temperature: float = 1.0,
        max_tokens: int = 256,
        top_p: float = 1.0,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
        api_key: Optional[str] = None,
    ):
        super().__init__(model_type=model_type, max_gen_tokens=max_tokens)
        self.temperature = temperature
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.tokenizer = TiktokenTokenizer(OPENAI_TOKENIZERS[self.model_type])

        try:
            self.openai_client = create_openai_client(api_key)
        except ValueError as e:
            warnings.warn(
                "OpenAI API key not provided, unable to create "
                + "OpenAI client. This means generating from "
                + f"this instance will be unavailable: {e}"
            )
            self.openai_client = None

    def get_config_dict(self) -> Dict[str, Any]:
        """Get the configuration dictionary for the LLM."""
        return {
            "temperature": self.temperature,
            "max_tokens": self.max_gen_tokens,
            "top_p": self.top_p,
            "frequency_penalty": self.frequency_penalty,
            "presence_penalty": self.presence_penalty,
        }

    def generate(
        self, messages: List[Message], stream: bool = False, **kwargs
    ) -> Union[str, Generator[str, None, None]]:
        """Generate text using the LLM."""
        message_dict = self._construct_api_messages(messages)

        try:
            response = self.openai_client.chat.completions.create(
                model=self.model_type.value,
                messages=message_dict,
                temperature=self.temperature,
                max_tokens=self.max_gen_tokens,
                top_p=self.top_p,
                frequency_penalty=self.frequency_penalty,
                presence_penalty=self.presence_penalty,
                stream=stream,
                **kwargs,
            )
        except OpenAIError as err:
            raise PromptModelError(self.model_type, err)

        if stream:
            return self._construct_stream_generator(response)
        else:
            return response.choices[0].message.content

    def _construct_stream_generator(
        self, response
    ) -> Generator[str, None, None]:
        for item in response:
            if item.choices[0].finish_reason:
                break

            yield item.choices[0].delta.content

    def _construct_api_messages(
        self, messages: List[Message]
    ) -> List[Dict[str, str]]:
        return [message.model_dump() for message in messages]
