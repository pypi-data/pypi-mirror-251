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


import random
import uuid

from ..utils.constants import MAX_INT


def generate_random_positive_int() -> int:
    """Generate a random integer between 0 and MAX_INT."""
    return random.randint(0, MAX_INT)


def generate_random_str(max_chars: int = 36) -> str:
    """Generate a random string of length max_chars."""
    return uuid.uuid4().hex[:max_chars]
