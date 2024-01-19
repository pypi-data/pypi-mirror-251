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


from typing import List, Optional

from ..embedding.embedding import Embedding
from ..embedding.embedding_vector import EmbeddingVector
from ..model_provider.openai import (
    OPENAI_TOKENIZERS,
    OpenAIEmbeddingModelType,
    create_openai_client,
)
from ..tokenizer.tiktoken_tokenizer import TiktokenTokenizer


class OpenAIEmbedding(Embedding):
    """OpenAIEmbedding is a Embedding that uses an OpenAI model to
    retrieve vector embeddings for text.

    Attributes:
        model_type: The type of the OpenAI embedding model to use.
        api_key (optional): The API key to use to access the OpenAI API. If
            this is not provided, the OPENAI_API_KEY environment variable
            will be used.
    """

    def __init__(
        self,
        model_type: OpenAIEmbeddingModelType = (
            OpenAIEmbeddingModelType.TEXT_EMBED_ADA_002
        ),
        api_key: Optional[str] = None,
    ):
        super().__init__(model_type=model_type)
        self.openai_client = create_openai_client(api_key)

        self.tokenizer = TiktokenTokenizer(OPENAI_TOKENIZERS[self.model_type])

    def embed_text_batch(self, texts: List[str]) -> List[EmbeddingVector]:
        """Embed the given texts into vector embeddings using the embedding
        model.
        """
        response = self.openai_client.embeddings.create(
            input=texts,
            model=self.model_type.value,
        )

        if not hasattr(response, "data"):
            raise RuntimeError(
                f"OpenAI API response did not contain data: {response}"
            )

        if len(response.data) != len(texts):
            raise RuntimeError(
                f"OpenAI API response data contained {len(response.data)} "
                + f"elements, but {len(texts)} were expected: {response}"
            )

        return [
            EmbeddingVector(vector=data.embedding) for data in response.data
        ]
