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


import os
from typing import List

from ..document.document import Document
from ..utils.functions import generate_random_str


class Dataset:
    """A Dataset is a representation of a collection of data
    that is used for ingestion and retrieval.

    Attributes:
        id (str): The ID of the dataset.
        documents (List[Document]): The documents associated with
            this dataset.
    """

    def __init__(
        self,
        documents: List[Document],
    ):
        self.documents = documents
        self.id = generate_random_str()

    @classmethod
    def from_directory(cls, directory_path: str):
        """Creates a Dataset from a directory of files.

        Args:
            directory_path (str): The path to the directory.
        """
        documents = []
        for file_name in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file_name)
            if os.path.isfile(file_path):
                with open(file_path, "r") as f:
                    doc_text = f.read()
                documents.append(Document(doc_text))

        return cls(documents)

    def add_document(self, document: Document):
        return self.add_documents([document])

    def add_documents(self, documents: List[Document]):
        self.documents.extend(documents)

    def get_documents(self) -> List[Document]:
        return self.documents

    def get_id(self) -> str:
        return self.id
