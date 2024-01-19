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
from typing import Dict, Optional, Union

import openai

OPENAI_ENV_VARIABLE = "OPENAI_API_KEY"


class OpenAIEmbeddingModelType(str, Enum):
    """OpenAI embedding mode model types."""

    TEXT_EMBED_ADA_002 = "text-embedding-ada-002"


class OpenAIModelType(str, Enum):
    """OpenAI LLM model types."""

    GPT_35_TURBO_INSTRUCT = "gpt-3.5-turbo-instruct"
    GPT_35_TURBO = "gpt-3.5-turbo"
    GPT_35_TURBO_16K = "gpt-3.5-turbo-16k"
    GPT_35_TURBO_1106 = "gpt-3.5-turbo-1106"
    GPT_4_32K = "gpt-4-32k"
    GPT_4 = "gpt-4"
    GPT_4_1106_PREVIEW = "gpt-4-1106-preview"


OPENAI_EMBED_INPUT_TOKEN_LIMITS: Dict[OpenAIEmbeddingModelType, int] = {
    OpenAIEmbeddingModelType.TEXT_EMBED_ADA_002: 8192,
}

OPENAI_EMBED_OUTPUT_DIMENSIONS: Dict[OpenAIEmbeddingModelType, int] = {
    OpenAIEmbeddingModelType.TEXT_EMBED_ADA_002: 1536,
}

OPENAI_TOKENIZERS: Dict[
    Union[OpenAIModelType, OpenAIEmbeddingModelType], str
] = {
    OpenAIEmbeddingModelType.TEXT_EMBED_ADA_002: "cl100k_base",
    OpenAIModelType.GPT_35_TURBO_INSTRUCT: "cl100k_base",
    OpenAIModelType.GPT_35_TURBO: "cl100k_base",
    OpenAIModelType.GPT_35_TURBO_16K: "cl100k_base",
    OpenAIModelType.GPT_35_TURBO_1106: "cl100k_base",
    OpenAIModelType.GPT_4_32K: "cl100k_base",
    OpenAIModelType.GPT_4: "cl100k_base",
    OpenAIModelType.GPT_4_1106_PREVIEW: "cl100k_base",
}

OPENAI_MODEL_MAX_TOKEN_LIMITS: Dict[OpenAIModelType, int] = {
    OpenAIModelType.GPT_35_TURBO_INSTRUCT: 4096,
    OpenAIModelType.GPT_35_TURBO: 4096,
    OpenAIModelType.GPT_35_TURBO_16K: 16385,
    OpenAIModelType.GPT_35_TURBO_1106: 16385,
    OpenAIModelType.GPT_4_32K: 32768,
    OpenAIModelType.GPT_4: 8192,
    OpenAIModelType.GPT_4_1106_PREVIEW: 128000,
}

OPENAI_MODEL_OVERHEAD_TOKENS_PER_MESSAGE: Dict[OpenAIModelType, int] = {
    OpenAIModelType.GPT_35_TURBO_INSTRUCT: 3,
    OpenAIModelType.GPT_35_TURBO: 3,
    OpenAIModelType.GPT_35_TURBO_16K: 3,
    OpenAIModelType.GPT_35_TURBO_1106: 3,
    OpenAIModelType.GPT_4_32K: 3,
    OpenAIModelType.GPT_4: 3,
    OpenAIModelType.GPT_4_1106_PREVIEW: 3,
}

OPENAI_MODEL_OVERHEAD_TOKENS_PER_RESPONSE: Dict[OpenAIModelType, int] = {
    OpenAIModelType.GPT_35_TURBO_INSTRUCT: 3,
    OpenAIModelType.GPT_35_TURBO: 3,
    OpenAIModelType.GPT_35_TURBO_16K: 3,
    OpenAIModelType.GPT_35_TURBO_1106: 3,
    OpenAIModelType.GPT_4_32K: 3,
    OpenAIModelType.GPT_4: 3,
    OpenAIModelType.GPT_4_1106_PREVIEW: 3,
}


def create_openai_client(
    api_key: Optional[str] = None,
) -> openai.OpenAI:
    """Create an OpenAI client with the given API key.

    Args:
        api_key (str, optional): The API key to use to access the OpenAI API.
            If this is not provided, the OPENAI_API_KEY environment variable
            will be used.
    """

    if api_key is None:
        api_key = os.getenv(OPENAI_ENV_VARIABLE, None)

    if api_key is None:
        raise ValueError(
            f"OpenAI API key not provided and {OPENAI_ENV_VARIABLE} "
            + "environment variable is not set."
        )

    return openai.OpenAI(api_key=api_key)
