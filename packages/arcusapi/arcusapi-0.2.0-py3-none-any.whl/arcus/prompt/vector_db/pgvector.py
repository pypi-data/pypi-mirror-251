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


import ast
import warnings
from typing import List, Optional

import psycopg
from pgvector.psycopg import register_vector

from ..embedding.embedding_vector import EmbeddingVector
from ..indexing.nearest_neighbor import SimilarityMode
from ..node.node import Node
from ..query.query import Query
from ..vector_db.vector_db_client import VectorDBClient

PROMPT_TABLE_NAME = "arcus_prompt_table"
MAX_PGVECTOR_INDEX_DIM = 2000


class PGVectorDBClient(VectorDBClient):
    """PGVectorDBClient is a vector database client that uses PostgreSQL
    and the pgvector extension. This client is used for both indexing and
    querying.

    Attributes:
        database (str): The name of the database.
        host (str): The host of the database.
        user (str): The user of the database.
        password (Optional[str]): The password of the database.
        port (int): The port of the database.
    """

    def __init__(
        self,
        database: str = "vectordb",
        host: str = "localhost",
        user: str = "user",
        password: Optional[str] = None,
        port: int = 5432,
    ):
        self.database = database
        self.host = host
        self.password = password
        self.port = port
        self.user = user
        self.conn = self._create_connection()

        self.table = None
        self.initialized = False

    def _check_if_table_name_exists(self, table_name: str) -> bool:
        """Check if the given table name exists in the database."""
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT EXISTS ("
                + "SELECT FROM information_schema.tables "
                + f"WHERE table_schema='public' AND table_name='{table_name}'"
                + ")"
            )
            return cur.fetchone()[0]

    def _create_connection_string(self) -> str:
        conn_string = (
            f"host={self.host} port={self.port} "
            + f"dbname={self.database} user={self.user}"
        )
        if self.password is not None:
            conn_string += f" password={self.password}"
        return conn_string

    def _create_connection(self) -> psycopg.Connection:
        return psycopg.connect(
            self._create_connection_string(), autocommit=True
        )

    def _pgvector_vector_to_list(self, vector) -> List[float]:
        if isinstance(vector, str):
            return ast.literal_eval(vector)
        else:
            return list(vector)

    def __del__(self):
        self.conn.close()

    def _create_schema(self, embed_dim: int):
        """Create the schema for the vector database."""
        with self.conn.cursor() as cur:
            register_vector(self.conn)

            cur.execute(
                f"CREATE TABLE {self.table} (application_id VARCHAR(36),"
                + "node_id BIGINT PRIMARY KEY, "
                + f"embedding vector({embed_dim}), content text)"
            )

    def _create_hnsw_index(self, similarity_mode: SimilarityMode):
        """Create the hnsw index for the vector database."""
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "CREATE INDEX "
                    + f"{self.table}_hnsw_{similarity_mode.value} "
                    + f"ON {self.table} USING hnsw (embedding "
                    + f"{self._get_similarity_vector_str(similarity_mode)})"
                )
        except psycopg.errors.UndefinedObject:
            warnings.warn(
                f"Failed to create hnsw index for table {self.table}. "
                + "Consider upgrading pgvector to version 0.5.0 or higher."
            )

    def _get_similarity_vector_str(self, similarity_mode: SimilarityMode):
        if similarity_mode == SimilarityMode.COSINE:
            return "vector_cosine_ops"
        elif similarity_mode == SimilarityMode.EUCLIDEAN:
            return "vector_l2_ops"
        elif similarity_mode == SimilarityMode.INNER_PRODUCT:
            return "vector_inner_product_ops"
        else:
            raise ValueError(f"Invalid similarity mode: {similarity_mode}")

    def _get_similarity_sql(self, similarity_mode: SimilarityMode):
        """Get the SQL for the similarity mode."""
        if similarity_mode == SimilarityMode.COSINE:
            return "<=>"
        elif similarity_mode == SimilarityMode.EUCLIDEAN:
            return "<->"
        elif similarity_mode == SimilarityMode.INNER_PRODUCT:
            return "<#>"
        else:
            raise ValueError(f"Invalid similarity mode: {similarity_mode}")

    def _gen_table_name(self, embed_dim: int):
        return f"{PROMPT_TABLE_NAME}_{embed_dim}"

    def test_connection(self) -> bool:
        try:
            self._create_connection()
            return True
        except Exception:
            return False

    def is_initialized(self) -> bool:
        """Check if the vector database is initialized, e.g. schema is
        created.
        """
        return self.initialized

    def initialize(self, embed_dim: int, similarity_mode: SimilarityMode):
        """Initialize the vector database, e.g. create schema."""
        self.table = self._gen_table_name(embed_dim)

        if self._check_if_table_name_exists(self.table):
            self.initialized = True

        if self.initialized:
            return

        self._create_schema(embed_dim)
        self._create_hnsw_index(similarity_mode)
        self.initialized = True

    def insert_node(self, node: Node, application_id: str):
        """Insert the given node into the vector database.

        Args:
            node (Node): The node to insert.
            application_id (str): The ID of the application inserting the node.
        """
        with self.conn.cursor() as cur:
            cur.execute(
                f"INSERT INTO {self.table} (application_id, node_id, "
                + "embedding, content) "
                + "VALUES (%s, %s, %s, %s)",
                (
                    application_id,
                    node.get_id(),
                    node.get_embedding_vector().get_vector(),
                    node.get_text(),
                ),
            )

    def query_nodes(self, query: Query, application_id: str) -> List[Node]:
        """ "Query the vector database for nodes matching the given query.

        Args:
            query (Query): The query to use to retrieve nodes.
            application_id (str): The ID of the application querying the nodes.

        Returns:
            List[Node]: The nodes matching the given query for the
                given application.
        """
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT node_id, embedding, content "
                + f"FROM {self.table} WHERE application_id='{application_id}' "
                + "ORDER BY embedding "
                + f"{self._get_similarity_sql(query.get_similarity_mode())} "
                + "%s::vector LIMIT %s",
                (
                    query.get_embedding_vector().get_vector(),
                    query.get_top_k(),
                ),
            )
            results = cur.fetchall()

        nodes = []
        for result in results:
            node = Node(
                id=result[0],
                embedding_vector=EmbeddingVector(
                    vector=self._pgvector_vector_to_list(result[1])
                ),
                text=result[2],
            )
            nodes.append(node)

        return nodes

    def max_vector_size(self) -> int:
        return MAX_PGVECTOR_INDEX_DIM
