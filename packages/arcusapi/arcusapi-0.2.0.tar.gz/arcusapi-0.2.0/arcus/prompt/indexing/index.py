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

from ..chunking.chunker import Chunker
from ..chunking.sentence_chunker import SentenceChunker
from ..dataset.dataset import Dataset
from ..document.document import Document
from ..embedding.embedding import Embedding
from ..indexing.nearest_neighbor import SimilarityMode
from ..node.node import Node
from ..query.query import Query
from ..vector_db.vector_db_client import VectorDBClient


class Index:
    """The Index class is responsible for indexing and querying data.

    Attributes:
        embedding (Embedding): The embedding model used for indexing and
            querying.
        vector_db_client (VectorDBClient): The vector database client used for
            indexing and querying.
        application_id (str): The ID of the application corresponding to this
            index.
    """

    def __init__(
        self,
        embedding: Embedding,
        vector_db_client: VectorDBClient,
        application_id: str,
    ):
        self.embedding = embedding
        self.vector_db_client = vector_db_client
        self.application_id = application_id

        if not self.vector_db_client.test_connection():
            raise ValueError(
                "VectorDBClient connection test failed for "
                + f"{self.vector_db_client.__class__.__name__}"
            )

        assert (
            self.vector_db_client.max_vector_size()
            >= self.embedding.get_output_dimensions()
        ), (
            f"VectorDBClient {self.vector_db_client.__class__.__name__} "
            + f"maximum vector size ({self.vector_db_client.max_vector_size()}"
            + ") must be greater than or equal "
            + f"to {self.embedding.__class__.__name__} "
            + f"output dimensions ({self.embedding.get_output_dimensions()})"
        )

        self.chunker = SentenceChunker(
            embedding.get_tokenizer(),
            embedding.get_max_input_tokens(),
        )
        self.similarity_mode = SimilarityMode.EUCLIDEAN

        self.vector_db_client.initialize(
            embedding.get_output_dimensions(), self.similarity_mode
        )

    def update(
        self,
        dataset: Dataset,
    ):
        """
        Update the index with the given dataset.

        Args:
            dataset (Dataset): The dataset to index.
        """
        dataset_id = dataset.get_id()
        for document in dataset.get_documents():
            self.update_document(document, dataset_id)

    def update_document(
        self,
        document: Document,
        dataset_id: str,
    ):
        """
        Update the index with the given document.

        Args:
            document (Document): The document to index.
            dataset_id (str): The ID of the dataset that the document belongs
                to.
        """
        document_id = document.get_id()
        chunks: List[str] = self.chunker.chunk(document.get_text())

        for chunk_text in chunks:
            chunk_embedding = self.embedding.embed_text(chunk_text)

            self.vector_db_client.insert_node(
                Node(
                    text=chunk_text,
                    document_id=document_id,
                    dataset_id=dataset_id,
                    embedding_vector=chunk_embedding,
                ),
                self.application_id,
            )

    def query(
        self,
        query: Query,
    ) -> List[Node]:
        """
        Query the index with the given query.

        Args:
            query (Query): The query to use to retrieve nodes.
        """

        return self.vector_db_client.query_nodes(query, self.application_id)

    def get_embedding(self) -> Embedding:
        """Get the embedding model used for indexing and querying."""
        return self.embedding

    def get_chunker(self) -> Chunker:
        """Get the sentence chunker used for indexing."""
        return self.chunker

    def get_similarity_mode(self) -> SimilarityMode:
        """Get the similarity mode used for indexing and querying."""
        return self.similarity_mode

    def get_application_id(self) -> str:
        """Get the ID of the application corresponding to this index."""
        return self.application_id
