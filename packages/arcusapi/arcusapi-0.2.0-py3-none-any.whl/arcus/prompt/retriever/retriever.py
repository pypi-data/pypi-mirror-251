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

from ..indexing.index import Index
from ..message.message import Message
from ..node.node import Node
from ..query.query import Query


class Retriever:
    """The Retriever class is responsible for retrieving data. The
    retriever is responsible for constructing queries from given text, and for
    returning post-processed results of the retrieved data.

    Attributes:
        index (Index): The index used for retrieval.
        top_k (int): The number of results to return for each query.
    """

    def __init__(
        self,
        index: Index,
        top_k: int = 5,
    ):
        self.index = index
        self.top_k = top_k
        self.embedding = index.get_embedding()
        self.chunker = index.get_chunker()

    def query(self, query_messages: List[Message]) -> List[Node]:
        """Retrieve nodes for a given prompt.

        Args:
            query_messages (List[Message]): The query messages to use to
                retrieve nodes.
        """
        query_text = query_messages[-1].content

        chunks: List[str] = self.chunker.chunk(query_text)

        query_text = chunks[-1]
        query_embedding = self.embedding.embed_text(query_text)

        query = Query(
            query_text,
            query_embedding,
            self.top_k,
            similarity_mode=self.index.get_similarity_mode(),
        )

        return self.index.query(query)
