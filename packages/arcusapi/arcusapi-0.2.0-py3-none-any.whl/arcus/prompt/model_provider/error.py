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


from ..model_provider.model_type import ModelType

PROMPT_ERROR_BASE = "Unable to generate response with model: "


class PromptModelError(Exception):
    """Base class for all model exceptions"""

    def __init__(self, model_type: ModelType, err: Exception):
        self.message = f"{PROMPT_ERROR_BASE}{model_type.value}"
        super().__init__(self.message, err)
