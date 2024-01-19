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

from arcus.client.client import ArcusClient

from ..mode.mode import Mode
from ..vector_db.vector_db_client import VectorDBClient


class SystemConfig:
    def __init__(
        self,
        mode: Mode = Mode.MANAGED,
        client: Optional[ArcusClient] = None,
        vector_db_client: Optional[VectorDBClient] = None,
    ):
        self.mode = mode
        if mode == Mode.LOCAL:
            assert vector_db_client is not None, (
                "A vector database client must be provided to create an"
                + " Arcus SystemConfig for local mode."
            )
        elif mode == Mode.MANAGED:
            assert client is not None, (
                "An Arcus client must be provided to create an Arcus"
                + " SystemConfig for managed mode. This client is used"
                + " to connect to the Arcus platform."
            )
        else:
            assert False, "Invalid mode: " + str(mode) + "."

        self.client = client
        self.vector_db_client = vector_db_client

    def get_mode(self) -> Mode:
        return self.mode

    def get_client(self) -> Optional[ArcusClient]:
        return self.client

    def get_vector_db_client(self) -> Optional[VectorDBClient]:
        return self.vector_db_client
