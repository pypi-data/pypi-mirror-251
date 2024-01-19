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


from collections import deque
from typing import List, Tuple

from ..chunking.chunker import Chunker
from ..chunking.split_chars import TEXT_SPLIT_CHARS
from ..tokenizer.tokenizer import Tokenizer


class SentenceChunker(Chunker):
    """SentenceChunker splits a text into discrete sentences, ensuring that
    the sentences do not exceed a maximum number of tokens.

    Attributes:
        tokenizer: The tokenizer to use to encode and decode text.
        max_chunk_tokens: The maximum number of tokens a chunk can have.
        sentence_separators: The characters that separate sentences. This is
            an ordered list, where splitting is prioritized in the order of
            the list.
    """

    def __init__(
        self,
        tokenizer: Tokenizer,
        max_chunk_tokens: int,
        sentence_separators: List[str] = TEXT_SPLIT_CHARS,
    ):
        self.tokenizer = tokenizer
        self.max_chunk_tokens = max_chunk_tokens
        self.sentence_separators = sentence_separators

    def _split_sentences(self, text: str, index: int) -> List[Tuple[str, int]]:
        """Split the given text into sentences using the sentence separator
        in the given index of the sentence separator list.
        """
        if index >= len(self.sentence_separators):
            return [
                (text[: len(text) // 2], index),
                (text[len(text) // 2 :], index),
            ]

        sentences: List[str] = text.split(self.sentence_separators[index])
        return [(sentence, index) for sentence in sentences]

    def chunk(self, document: str) -> List[str]:
        sentences: List[Tuple[str, int]] = self._split_sentences(document, 0)
        final_chunks: List[str] = []

        sentence_queue: deque = deque(sentences)

        while len(sentence_queue) > 0:
            sentence, index = sentence_queue.popleft()
            tokens: List[int] = self.tokenizer.encode(sentence)
            if len(tokens) > self.max_chunk_tokens:
                split_sentences = self._split_sentences(sentence, index + 1)

                for split_sentence, split_index in split_sentences:
                    sentence_queue.appendleft((split_sentence, split_index))
            else:
                continue_adding = len(sentence_queue) > 0
                while continue_adding:
                    next_sentence, next_index = sentence_queue[0]
                    next_sentence = (
                        self.sentence_separators[next_index] + next_sentence
                    )
                    next_tokens = self.tokenizer.encode(next_sentence)

                    if len(tokens) + len(next_tokens) > self.max_chunk_tokens:
                        continue_adding = False
                    else:
                        sentence_queue.popleft()
                        sentence += next_sentence
                        tokens += next_tokens

                    if len(sentence_queue) == 0:
                        continue_adding = False

                assert (
                    len(self.tokenizer.encode(sentence))
                    <= self.max_chunk_tokens
                ), (
                    "Sentence chunk token length "
                    + f"({len(self.tokenizer.encode(sentence))}) is larger "
                    + f"than max_chunk_tokens ({self. max_chunk_tokens})."
                )
                final_chunks.append(sentence)

        return final_chunks
