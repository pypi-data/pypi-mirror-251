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


from typing import Dict, Union

from ..model_provider.anthropic import (
    ANTHROPIC_MODEL_MAX_TOKEN_LIMITS,
    ANTHROPIC_MODEL_OVERHEAD_TOKENS_PER_MESSAGE,
    ANTHROPIC_MODEL_OVERHEAD_TOKENS_PER_RESPONSE,
    AnthropicModelType,
)
from ..model_provider.cohere import (
    COHERE_MODEL_MAX_TOKEN_LIMITS,
    COHERE_MODEL_OVERHEAD_TOKENS_PER_MESSAGE,
    COHERE_MODEL_OVERHEAD_TOKENS_PER_RESPONSE,
    COHERE_TOKENIZERS,
    CohereModelType,
)
from ..model_provider.openai import (
    OPENAI_EMBED_INPUT_TOKEN_LIMITS,
    OPENAI_EMBED_OUTPUT_DIMENSIONS,
    OPENAI_MODEL_MAX_TOKEN_LIMITS,
    OPENAI_MODEL_OVERHEAD_TOKENS_PER_MESSAGE,
    OPENAI_MODEL_OVERHEAD_TOKENS_PER_RESPONSE,
    OPENAI_TOKENIZERS,
    OpenAIEmbeddingModelType,
    OpenAIModelType,
)

ModelType = Union[
    AnthropicModelType,
    CohereModelType,
    OpenAIModelType,
]

EmbeddingModelType = OpenAIEmbeddingModelType


EMBED_INPUT_TOKEN_LIMITS: Dict[EmbeddingModelType, int] = {
    **OPENAI_EMBED_INPUT_TOKEN_LIMITS,
}

EMBED_OUTPUT_DIMENSIONS: Dict[EmbeddingModelType, int] = {
    **OPENAI_EMBED_OUTPUT_DIMENSIONS,
}

TOKENIZERS: Dict[Union[ModelType, EmbeddingModelType], str] = {
    **OPENAI_TOKENIZERS,
    **COHERE_TOKENIZERS,
}

MODEL_MAX_TOKEN_LIMITS: Dict[ModelType, int] = {
    **OPENAI_MODEL_MAX_TOKEN_LIMITS,
    **COHERE_MODEL_MAX_TOKEN_LIMITS,
    **ANTHROPIC_MODEL_MAX_TOKEN_LIMITS,
}

MODEL_OVERHEAD_TOKENS_PER_MESSAGE: Dict[ModelType, int] = {
    **OPENAI_MODEL_OVERHEAD_TOKENS_PER_MESSAGE,
    **COHERE_MODEL_OVERHEAD_TOKENS_PER_MESSAGE,
    **ANTHROPIC_MODEL_OVERHEAD_TOKENS_PER_MESSAGE,
}

MODEL_OVERHEAD_TOKENS_PER_RESPONSE: Dict[ModelType, int] = {
    **OPENAI_MODEL_OVERHEAD_TOKENS_PER_RESPONSE,
    **COHERE_MODEL_OVERHEAD_TOKENS_PER_RESPONSE,
    **ANTHROPIC_MODEL_OVERHEAD_TOKENS_PER_RESPONSE,
}
