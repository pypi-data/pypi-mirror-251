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
from typing import Any, Dict, List, Optional, Union

from ..message.message import Message
from ..model_provider.model_type import (
    MODEL_MAX_TOKEN_LIMITS,
    MODEL_OVERHEAD_TOKENS_PER_MESSAGE,
    MODEL_OVERHEAD_TOKENS_PER_RESPONSE,
    ModelType,
)
from ..tokenizer.tokenizer import Tokenizer


class LLM(ABC):
    """LLM is the abstract base class for all language model classes. The
    LLM is an abstraction that only makes LLM calls, it is not
    responsible for augmenting a user-generated prompt.
    """

    def __init__(
        self, model_type: ModelType, max_gen_tokens: Optional[int] = None
    ):
        self.model_type = model_type
        self.max_gen_tokens = max_gen_tokens

    @abstractmethod
    def generate(
        self, messages: List[Message], stream: bool = False, **kwargs
    ) -> Union[str, Generator[str, None, None]]:
        pass

    @abstractmethod
    def get_config_dict(self) -> Dict[str, Any]:
        """Get the configuration dictionary for the LLM."""
        pass

    def get_model_type(self) -> ModelType:
        """Get the model type of the LLM."""
        return self.model_type

    def get_tokenizer(self) -> Tokenizer:
        """Get the tokenizer used by the LLM."""
        if self.tokenizer is None:
            raise ValueError("Tokenizer not implemented for this LLM type.")
        return self.tokenizer

    def get_context_window(self) -> int:
        """Get the context window size for the LLM."""
        return MODEL_MAX_TOKEN_LIMITS[self.model_type]

    def get_max_generation_tokens(self) -> Optional[int]:
        """Get the maximum number of tokens that can be generated."""
        return self.max_gen_tokens

    def get_overhead_tokens_per_message(self) -> int:
        """Get the number of overhead tokens per message. This is used to
        represent the additional tokens by e.g. indicating the role of a
         message."""
        return MODEL_OVERHEAD_TOKENS_PER_MESSAGE[self.model_type]

    def get_overhead_tokens_per_response(self) -> int:
        """Get the number of overhead tokens per response. This is used to
        represent the additional tokens by e.g. indicating the role of a
         message in the LLM response."""
        return MODEL_OVERHEAD_TOKENS_PER_RESPONSE[self.model_type]

    def get_max_input_tokens(self) -> int:
        """Get the maximum number of tokens that can be input to the LLM."""
        max_gen_tokens = self.get_max_generation_tokens()

        if max_gen_tokens is None:
            return self.get_context_window()

        return self.get_context_window() - max_gen_tokens
