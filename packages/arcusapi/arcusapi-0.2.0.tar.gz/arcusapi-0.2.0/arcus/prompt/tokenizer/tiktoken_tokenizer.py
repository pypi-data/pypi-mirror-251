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

import tiktoken

from ..tokenizer.tokenizer import Tokenizer


class TiktokenTokenizer(Tokenizer):
    """TiktokenTokenizer encodes and decodes text into tokens using the
    TikToken library.
    """

    def __init__(self, model_name: str):
        self.tokenizer: tiktoken.Encoding = tiktoken.get_encoding(model_name)

    def encode(self, text: str) -> List[int]:
        """Encode the given text into tokens."""
        return self.tokenizer.encode_ordinary(text)

    def decode(self, tokens: List[int]) -> str:
        """Decode the given tokens into text."""
        return self.tokenizer.decode(tokens)
