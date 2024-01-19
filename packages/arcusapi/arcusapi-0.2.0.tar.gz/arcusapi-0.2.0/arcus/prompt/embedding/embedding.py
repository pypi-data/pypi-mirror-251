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

from ..embedding.embedding_vector import EmbeddingVector
from ..model_provider.model_type import (
    EMBED_INPUT_TOKEN_LIMITS,
    EMBED_OUTPUT_DIMENSIONS,
    EmbeddingModelType,
)
from ..tokenizer.tokenizer import Tokenizer

DEFAULT_EMBED_BATCH_SIZE = 64


class Embedding(ABC):
    """The Embedding interface retrieves vector embeddings for text."""

    def __init__(self, model_type: EmbeddingModelType):
        self.model_type = model_type

    @abstractmethod
    def embed_text_batch(self, texts: List[str]) -> List[EmbeddingVector]:
        pass

    def get_tokenizer(self) -> Tokenizer:
        return self.tokenizer

    def get_max_input_tokens(self) -> int:
        """Get the maximum number of tokens that can be input into the
        embedding at once.
        """
        return EMBED_INPUT_TOKEN_LIMITS[self.model_type]

    def get_output_dimensions(self) -> int:
        """Get the number of dimensions of the output vector embeddings."""
        return EMBED_OUTPUT_DIMENSIONS[self.model_type]

    def embed_text(self, text: str) -> EmbeddingVector:
        """Embed the given text into a vector embedding using the embedding
        model.
        """
        return self.embed_text_batch([text])[0]

    def embed_texts(
        self, texts: List[str], batch_size: int = DEFAULT_EMBED_BATCH_SIZE
    ) -> List[EmbeddingVector]:
        """Embed the given texts into vector embeddings using the
        embedding model.
        """
        embeddings = []
        for i in range(0, len(texts), batch_size):
            embeddings += self.embed_text_batch(
                texts[i : min(i + batch_size, len(texts))]
            )

        return embeddings
