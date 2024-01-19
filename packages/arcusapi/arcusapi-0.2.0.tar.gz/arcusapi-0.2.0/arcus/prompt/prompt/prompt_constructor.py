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
from typing import List

from ..message.message import Message
from ..node.node import Node
from ..tokenizer.tokenizer import Tokenizer


class PromptConstructor(ABC):
    """The PromptConstructor constructs prompts for the LLM given a
    context and an original prompt.
    """

    @abstractmethod
    def construct_prompt(
        self,
        nodes_context: List[Node],
        prompt: List[Message],
        tokenizer: Tokenizer,
        max_tokens: int,
        overhead_tokens_per_message: int,
    ) -> List[Message]:
        pass
