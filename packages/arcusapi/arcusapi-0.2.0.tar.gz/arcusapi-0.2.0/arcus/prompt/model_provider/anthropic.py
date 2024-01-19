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

import anthropic

ANTHROPIC_ENV_VARIABLE = "ANTHROPIC_API_KEY"


class AnthropicModelType(str, Enum):
    """Anthropic LLM model types."""

    CLAUDE = "claude-2.1"
    CLAUDE_INSTANT = "claude-instant-1.2"


ANTHROPIC_MODEL_MAX_TOKEN_LIMITS: Dict[AnthropicModelType, int] = {
    AnthropicModelType.CLAUDE: 200000,
    AnthropicModelType.CLAUDE_INSTANT: 100000,
}

ANTHROPIC_MODEL_OVERHEAD_TOKENS_PER_MESSAGE: Dict[AnthropicModelType, int] = {
    AnthropicModelType.CLAUDE: 8,
    AnthropicModelType.CLAUDE_INSTANT: 8,
}

ANTHROPIC_MODEL_OVERHEAD_TOKENS_PER_RESPONSE: Dict[AnthropicModelType, int] = {
    AnthropicModelType.CLAUDE: 0,
    AnthropicModelType.CLAUDE_INSTANT: 0,
}


def create_anthropic_client(
    api_key: Optional[str] = None,
) -> anthropic.Client:
    """Create a Anthropic client with the given API key.

    Args:
        api_key (str, optional): The API key to use to access the Anthropic
            API. If this is not provided, the ANTHROPIC_API_KEY environment
            variable will be used.
    """

    if api_key is None:
        api_key = os.getenv(ANTHROPIC_ENV_VARIABLE, None)

    if api_key is None:
        raise ValueError(
            f"Anthropic API key not provided and {ANTHROPIC_ENV_VARIABLE} "
            + "environment variable is not set."
        )

    return anthropic.Anthropic(api_key=api_key)
