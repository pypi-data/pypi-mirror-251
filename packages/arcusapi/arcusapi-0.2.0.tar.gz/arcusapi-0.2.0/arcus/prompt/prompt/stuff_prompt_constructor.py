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


from typing import List

from ..message.message import Message
from ..node.node import Node
from ..prompt.prompt_constructor import PromptConstructor
from ..tokenizer.tokenizer import Tokenizer

DEFAULT_STUFF_CONTEXT_PROMPT = (
    "Given the context, answer the following prompt. "
    + "Use ample specific details from the context, the more the "
    + "better. Don't use irrelevant context. If you don't know the answer, "
    + "just write 'I don't know, could you please ask again with additional "
    + "context or make your question more specific?'"
)


class StuffPromptConstructor(PromptConstructor):
    """The StuffPromptConstructor constructs prompts for the LLM given a
    context and an original prompt by stuffing the context into the prompt.
    """

    def __init__(
        self,
        context_prompt: str = DEFAULT_STUFF_CONTEXT_PROMPT,
    ):
        self.context_prompt = context_prompt

    def construct_prompt(
        self,
        nodes_context: List[Node],
        prompt: List[Message],
        tokenizer: Tokenizer,
        max_tokens: int,
        overhead_tokens_per_message: int,
    ) -> List[Message]:
        """Construct a prompt for the LLM given a context and an original
        prompt. Ensure that the prompt is not longer than the given maximum
        number of tokens.

        Args:
            nodes_context: The context nodes to use.
            prompt: The prompt to use.
            tokenizer: The tokenizer to use.
            max_tokens: The maximum number of tokens to use in the prompt.
            overhead_tokens_per_message: The number of overhead tokens per
                message. This is used to represent the additional tokens by
                e.g. indicating the role of a message.
        """
        new_messages = prompt.copy()
        new_messages[-1].content = (
            self.context_prompt + "\n\n" + new_messages[-1].content
        )

        num_tokens = sum(
            [
                tokenizer.get_token_count(message.content)
                for message in new_messages
            ]
        ) + overhead_tokens_per_message * len(new_messages)

        for node in nodes_context:
            next_context = node.get_text() + "\n\n"
            next_num_tokens = tokenizer.get_token_count(next_context)

            if num_tokens + next_num_tokens > max_tokens:
                break

            new_messages[-1].content = next_context + new_messages[-1].content
            num_tokens += next_num_tokens

        return new_messages
