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


from typing import Dict, List, Optional

from arcus.client.client import ArcusClient

from ..dataset.dataset import Dataset
from ..engine.config import EngineConfig, create_default_local_engine_config
from ..engine.engine import ClientEngine, Engine, LocalEngine
from ..mode.mode import Mode
from ..system.config import SystemConfig
from ..vector_db.vector_db_client import VectorDBClient


class System:
    def __init__(self, config: SystemConfig):
        self.config = config
        self.mode = config.get_mode()

        self.engines: Dict[int, LocalEngine] = {}
        self.datasets: List[Dataset] = []

    def get_vector_db_client(self) -> Optional[VectorDBClient]:
        return self.config.get_vector_db_client()

    def get_client(self) -> Optional[ArcusClient]:
        return self.config.get_client()

    def get_engine(self, engine_config: EngineConfig) -> Engine:
        if self.mode == Mode.LOCAL:
            application_id = engine_config.get_application_id()

            assert (
                application_id is not None
            ), "Application ID must be set to get Engine."

            if application_id not in self.engines:
                self.engines[application_id] = LocalEngine(
                    self.config,
                    engine_config,
                )

        elif self.mode == Mode.MANAGED:
            application_id = engine_config.get_application_id()

            if application_id not in self.engines:
                self.engines[application_id] = ClientEngine(
                    self.config,
                    engine_config,
                )
        else:
            raise ValueError("Invalid mode: " + str(self.mode) + ".")

        return self.engines[application_id]

    def create_engine(
        self,
        engine_config: EngineConfig = create_default_local_engine_config(),
    ) -> Engine:
        if self.mode == Mode.LOCAL:
            application_id = engine_config.get_application_id()

            if application_id is None:
                application_id = engine_config.create_application_id()

            assert (
                application_id not in self.engines
            ), f"Application ID {application_id} already exists."

            engine = LocalEngine(
                self.config,
                engine_config,
            )

            self._ingest_engine(engine)
            self.engines[application_id] = engine
            return engine
        else:
            raise NotImplementedError(
                "Please create an application for managed mode through the"
                + " Arcus platform."
            )

    def _ingest_engine(self, engine: LocalEngine):
        for dataset in self.datasets:
            engine.update_index([dataset])

    def ingest(self, datasets: List[Dataset]):
        if self.mode == Mode.LOCAL:
            self.datasets.extend(datasets)
            for engine in self.engines.values():
                self._ingest_engine(engine)
        else:
            raise ValueError(
                "Ingestion of datasets through the Arcus SDK is not supported"
                + " by the client. Please use the Arcus platform to "
                + "ingest datasets."
            )
