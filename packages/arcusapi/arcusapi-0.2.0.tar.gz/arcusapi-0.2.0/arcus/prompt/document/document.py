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


from ..utils.functions import generate_random_str


class Document:
    """A Document is a single unit of text.

    Attributes:
        id (str): The ID of the document.
        text (str): The text corresponding to the document.
    """

    def __init__(
        self,
        text: str,
    ):
        self.text = text
        self.id = generate_random_str()

    def get_text(self) -> str:
        """Get the text for this Document."""
        return self.text

    def get_id(self) -> str:
        """Get the ID for this Document."""
        return self.id
