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


from ..embedding.embedding_vector import EmbeddingVector
from ..indexing.nearest_neighbor import SimilarityMode


class Query:
    """A Query is a representation of a query that is used for retrieval.

    Attributes:
        text (str): The text corresponding to the query.
        embedding_vector (EmbeddingVector): The embedding vector
            corresponding to the query.
    """

    def __init__(
        self,
        text: str,
        embedding_vector: EmbeddingVector,
        top_k: int = 5,
        similarity_mode: SimilarityMode = SimilarityMode.EUCLIDEAN,
    ):
        self.text = text
        self.embedding_vector = embedding_vector
        self.top_k = top_k
        self.similarity_mode = similarity_mode

    def get_text(self) -> str:
        """Get the text for this Query."""
        return self.text

    def get_embedding_vector(self) -> EmbeddingVector:
        """Get the embedding vector for this Query."""
        return self.embedding_vector

    def get_top_k(self) -> int:
        """Get the number of results to return for this Query."""
        return self.top_k

    def get_similarity_mode(self) -> SimilarityMode:
        """Get the similarity mode for this Query."""
        return self.similarity_mode

    def __str__(self) -> str:
        return (
            f"Query(text={self.text}, "
            + f"embedding_vector={self.embedding_vector}"
            + f"top_k={self.top_k}"
            + f"similarity_mode={self.similarity_mode})"
        )

    def __repr__(self) -> str:
        return self.__str__()
