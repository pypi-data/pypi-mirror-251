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

from anthropic import AI_PROMPT, HUMAN_PROMPT
from anthropic import Anthropic as AnthropicClient
from anthropic import AnthropicError

from ..llm.llm import LLM
from ..message.message import Message
from ..model_provider.anthropic import (
    AnthropicModelType,
    create_anthropic_client,
)
from ..model_provider.error import PromptModelError
from ..tokenizer.anthropic_tokenizer import AnthropicTokenizer


class Anthropic(LLM):
    """Access wrapper around a Anthropic LLM model using their generate api.
    Details of the api can be seen at:
    https://docs.anthropic.com/reference/generate.

    Attributes:
        model_type: The type of Anthropic LLM to use. See AnthropicModelType
            for a list of supported options.
        temperature: The temperature to use for the LLM.
        max_tokens: The maximum number of tokens to generate.
        top_p: The top_p to use for the LLM.
        api_key (optional): The API key to use to access the Anthropic API. If
            this is not provided, the ANTHROPIC_API_KEY environment variable
            will be used.
    """

    def __init__(
        self,
        model_type: AnthropicModelType = AnthropicModelType.CLAUDE,
        temperature: float = 1,
        max_tokens: int = 256,
        top_p: float = 0.7,
        api_key: Optional[str] = None,
    ):
        super().__init__(model_type=model_type, max_gen_tokens=max_tokens)
        self.temperature = temperature
        self.top_p = top_p

        try:
            self.anthropic_client = create_anthropic_client(api_key)
        except AnthropicError as e:
            warnings.warn(
                "Anthropic API key not provided, unable to create "
                + "Anthropic client. This means generating from "
                + f"this instance will be unavailable: {e}"
            )
            self.anthropic_client = AnthropicClient()

        self.tokenizer = AnthropicTokenizer(client=self.anthropic_client)

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
        final_prompt = self._construct_api_prompt(messages)

        try:
            response = self.anthropic_client.completions.create(
                prompt=final_prompt,
                model=self.model_type.value,
                temperature=self.temperature,
                max_tokens_to_sample=self.max_gen_tokens,
                top_p=self.top_p,
                stream=stream,
                **kwargs,
            )

        except AnthropicError as err:
            raise PromptModelError(self.model_type, err)

        if stream:
            return self._construct_stream_generator(response)
        else:
            return response.completion

    def _construct_stream_generator(
        self, response
    ) -> Generator[str, None, None]:
        for item in response:
            yield item.completion

    def _construct_api_prompt(self, messages: List[Message]) -> str:
        """Construct the prompt to use for the API call."""

        prompt = ""
        for message in messages:
            if message.role == "user":
                prompt += f"{HUMAN_PROMPT}{message.content}"
            elif message.role == "assistant":
                prompt += f"{AI_PROMPT}{message.content}"
            elif message.role == "system":
                # Anthropic does not support system messages. See:
                # https://docs.anthropic.com/claude/docs/
                # how-to-use-system-prompts
                # #legacy-system-prompts-via-text-completions-api
                prompt += f"{message.content}\n\n"
            else:
                raise ValueError(
                    f"Message role {message.role} is not supported for "
                    + "Anthropic LLM."
                )

        return f"{prompt}{AI_PROMPT}"
