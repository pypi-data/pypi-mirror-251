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
from enum import Enum
from typing import Dict, Optional

import cohere

COHERE_ENV_VARIABLE = "COHERE_API_KEY"


class CohereModelType(str, Enum):
    """Cohere LLM model types."""

    COMMAND = "command"
    COMMAND_NIGHTLY = "command-nightly"
    COMMAND_LIGHT = "command-light"
    COMMAND_LIGHT_NIGHTLY = "command-light-nightly"


COHERE_TOKENIZERS: Dict[CohereModelType, str] = {
    CohereModelType.COMMAND: "command-nightly",
    CohereModelType.COMMAND_NIGHTLY: "command-nightly",
    CohereModelType.COMMAND_LIGHT: "command-nightly",
    CohereModelType.COMMAND_LIGHT_NIGHTLY: "command-nightly",
}

COHERE_MODEL_MAX_TOKEN_LIMITS: Dict[CohereModelType, int] = {
    CohereModelType.COMMAND: 4096,
    CohereModelType.COMMAND_NIGHTLY: 4096,
    CohereModelType.COMMAND_LIGHT: 4096,
    CohereModelType.COMMAND_LIGHT_NIGHTLY: 4096,
}

COHERE_MODEL_OVERHEAD_TOKENS_PER_MESSAGE: Dict[CohereModelType, int] = {
    CohereModelType.COMMAND: 0,
    CohereModelType.COMMAND_NIGHTLY: 0,
    CohereModelType.COMMAND_LIGHT: 0,
    CohereModelType.COMMAND_LIGHT_NIGHTLY: 0,
}

COHERE_MODEL_OVERHEAD_TOKENS_PER_RESPONSE: Dict[CohereModelType, int] = {
    CohereModelType.COMMAND: 0,
    CohereModelType.COMMAND_NIGHTLY: 0,
    CohereModelType.COMMAND_LIGHT: 0,
    CohereModelType.COMMAND_LIGHT_NIGHTLY: 0,
}


def create_cohere_client(
    api_key: Optional[str] = None,
) -> cohere.Client:
    """Create a Cohere client with the given API key.

    Args:
        api_key (str, optional): The API key to use to access the Cohere API.
            If this is not provided, the COHERE_API_KEY environment variable
            will be used.
    """

    if api_key is None:
        api_key = os.getenv(COHERE_ENV_VARIABLE, None)

    if api_key is None:
        raise ValueError(
            f"Cohere API key not provided and {COHERE_ENV_VARIABLE} "
            + "environment variable is not set."
        )

    return cohere.Client(api_key)
