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


from typing import Optional

from pydantic import BaseModel, Field

from ..embedding.embedding_vector import EmbeddingVector
from ..utils.functions import generate_random_positive_int


class Node(BaseModel):
    """A Node is a single unit of data retrieval.

    Attributes:
        text: The text corresponding to the node.
        document_id: The document ID corresponding to this node.
        dataset_id: The dataset ID corresponding to this node.
        id: The ID of the node.
        embedding_vector: The embedding representation of the node.
    """

    text: str
    document_id: Optional[str] = None
    dataset_id: Optional[str] = None
    id: Optional[int] = Field(default_factory=generate_random_positive_int)
    embedding_vector: Optional[EmbeddingVector] = None

    def get_id(self) -> int:
        """Get the ID of this Node."""
        return self.id

    def get_document_id(self) -> Optional[str]:
        """Get the document ID corresponding to this Node."""
        return self.document_id

    def get_dataset_id(self) -> Optional[str]:
        """Get the dataset ID corresponding to this Node."""
        return self.dataset_id

    def set_embedding_vector(self, embedding_vector: EmbeddingVector):
        """Set the embedding values for this Node."""
        self.embedding_vector = embedding_vector

    def get_embedding_vector(self) -> Optional[EmbeddingVector]:
        """Get the embedding values for this Node."""
        return self.embedding_vector

    def get_text(self) -> str:
        """Get the text for this Node."""
        return self.text

    def set_text(self, text: str):
        """Set the text for this Node."""
        self.text = text

    def __str__(self) -> str:
        s = f"Node(id={self.id}, text={self.text}"
        if self.document_id:
            s += f", document_id={self.document_id}"
        if self.dataset_id:
            s += f", dataset_id={self.dataset_id}"
        if self.embedding_vector:
            s += f", embedding_vector={self.embedding_vector}"
        s += ")"
        return s

    def __repr__(self) -> str:
        return str(self.id)

    def __hash__(self) -> int:
        return hash(self.id)
