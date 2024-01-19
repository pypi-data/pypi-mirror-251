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


class Chunker(ABC):
    """The Chunker interface chunks text into chunks."""

    @abstractmethod
    def chunk(self, document: str) -> List[str]:
        pass

    def chunk_documents(self, documents: List[str]) -> List[str]:
        """Chunk the given documents into chunks using the chunker."""
        chunks = []
        for document in documents:
            chunks += self.chunk(document)
        return chunks
