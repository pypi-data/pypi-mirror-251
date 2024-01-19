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


from typing import Any, Dict

from pydantic import BaseModel

from ..llm.anthropic import Anthropic
from ..llm.cohere import Cohere
from ..llm.llm import LLM
from ..llm.openai import OpenAI
from ..model_provider.model_type import (
    AnthropicModelType,
    CohereModelType,
    ModelType,
    OpenAIModelType,
)


class LLMConfig(BaseModel):
    llm_type: ModelType
    config_dict: Dict[str, Any]


def llm_from_config(config: LLMConfig) -> LLM:
    model_type = config.llm_type
    config_dict = config.config_dict

    if isinstance(model_type, OpenAIModelType):
        return OpenAI(
            model_type=model_type,
            **config_dict,
        )
    elif isinstance(model_type, CohereModelType):
        return Cohere(
            model_type=model_type,
            **config_dict,
        )
    elif isinstance(model_type, AnthropicModelType):
        return Anthropic(
            model_type=model_type,
            **config_dict,
        )

    raise ValueError(
        f"Invalid model type provided to LLM constructor: {model_type}"
    )


def llm_to_config(llm: LLM) -> LLMConfig:
    return LLMConfig(
        llm_type=llm.model_type,
        config_dict=llm.get_config_dict(),
    )
