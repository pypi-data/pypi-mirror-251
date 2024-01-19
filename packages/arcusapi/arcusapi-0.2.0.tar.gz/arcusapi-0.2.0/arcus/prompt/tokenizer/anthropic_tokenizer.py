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

from anthropic import Anthropic

from ..tokenizer.tokenizer import Tokenizer


class AnthropicTokenizer(Tokenizer):
    """Anthropic tokenizer used by the Command-Nightly LLM model."""

    def __init__(self, client: Anthropic = None):
        self.client = client if client else Anthropic()
        self.tokenizer = self.client.get_tokenizer()

    def encode(self, text: str) -> List[int]:
        """Encode the given text into tokens."""
        return self.tokenizer.encode(text).ids

    def decode(self, tokens: List[int]) -> str:
        """Decode the given tokens into text."""
        return self.tokenizer.decode(tokens)
