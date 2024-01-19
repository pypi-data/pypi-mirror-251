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

from ..indexing.nearest_neighbor import SimilarityMode
from ..node.node import Node
from ..query.query import Query


class VectorDBClient(ABC):
    """VectorDBClient is the abstract base class for all vector database
    clients. The VectorDBClient is an abstraction that only makes vector
    database calls.
    """

    @abstractmethod
    def test_connection(self) -> bool:
        """Test the connection to the vector database."""
        pass

    @abstractmethod
    def is_initialized(self, *args, **kwargs) -> bool:
        """Check if the vector database is initialized, e.g. schema is
        created.
        """
        pass

    @abstractmethod
    def initialize(
        self, embed_dim: int, similarity_mode: SimilarityMode, *args, **kwargs
    ):
        """Initialize the vector database, e.g. create schema and indexes."""
        pass

    @abstractmethod
    def insert_node(self, node: Node, application_id: str):
        """Insert the given node into the vector database."""
        pass

    @abstractmethod
    def query_nodes(self, query: Query, application_id: str) -> List[Node]:
        """Query the vector database for nodes matching the given query."""
        pass

    @abstractmethod
    def max_vector_size(self) -> int:
        """Get the maximum vector size supported by the vector database."""
        pass
