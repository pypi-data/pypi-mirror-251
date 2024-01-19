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


import warnings
from typing import Dict, Optional

import requests
from arcus.env.env import ARCUS_URL
from requests.adapters import HTTPAdapter, Retry

BEARER_PREFIX = "Bearer "

BACKOFF_TIME = 0.5
DISALLOWED_STATUS_CODES = [
    status for status in requests.status_codes._codes if status >= 400
]
RETRIABLE_METHODS = frozenset(
    ["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "POST"]
)


class ArcusResponse:
    """
    Wrapper around the response from an Arcus API call. Encodes whether status
    code was okay and the data returned.
    """

    data: Optional[dict]
    status_ok: bool

    def __init__(self, status_ok: bool, data: Optional[dict] = None):
        self.data = data
        self.status_ok = status_ok


class ArcusClient:
    """
    Base class for API clients to Arcus. Provides a common interface for
    making requests to the Arcus API.
    """

    def __init__(self, api_key: str, num_retries: int = 5):
        self.api_key = api_key
        self.num_retries = num_retries
        self.retry_session = None
        self.non_retry_session = None

        self.retry_session = self._get_retry_session()
        self.non_retry_session = self._get_non_retry_session()

    def _get_non_retry_session(self) -> requests.Session:
        if self.non_retry_session:
            return self.non_retry_session

        return requests.Session()

    def _get_retry_session(self) -> requests.Session:
        if self.retry_session:
            return self.retry_session

        session = requests.Session()
        retry = Retry(
            total=self.num_retries,
            backoff_factor=BACKOFF_TIME,
            raise_on_redirect=False,
            raise_on_status=False,
            status_forcelist=DISALLOWED_STATUS_CODES,
            allowed_methods=RETRIABLE_METHODS,
        )
        session.mount(
            "https://",
            HTTPAdapter(max_retries=retry),
        )
        session.mount(
            "http://",
            HTTPAdapter(max_retries=retry),
        )

        return session

    def _create_auth_headers(self) -> Dict:
        return {
            "Authorization": BEARER_PREFIX + self.api_key,
        }

    def _append_auth_header(self, headers: Optional[Dict] = None) -> Dict:
        """
        Given a set of headers, construct a new set of headers with the
        authentication headers added.
        """
        if headers is None:
            return self._create_auth_headers()

        headers.update(self._create_auth_headers())
        return headers

    def request(
        self,
        method: str,
        path: str,
        params: Optional[Dict] = None,
        json: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        retryable: bool = False,
    ) -> ArcusResponse:
        """
        Wrapper around requests.request that adds authentication headers and
        raises warnings in the case of errors.
        Args:
            method: HTTP method to use.
            path: Path to append to the base URL.
            params: Query parameters to pass to the request.
            json: JSON body to pass to the request.
            headers: Headers to pass to the request.
            retryable: Whether the request is retryable.
        Returns:
            ArcusResponse object containing the response data and whether the
            status code was okay.
        """

        headers = self._append_auth_header(headers)

        if retryable:
            session = self._get_retry_session()
        else:
            session = self._get_non_retry_session()

        response = session.request(
            method,
            f"{ARCUS_URL}/{path}",
            params=params,
            json=json,
            headers=headers,
        )

        if not response.ok:
            warnings.warn(
                f"Request {method} {ARCUS_URL}/{path} failed with "
                + f"status code {response.status_code} and message "
                + f"{response.text}."
            )

        return ArcusResponse(
            data=response.json() if response.ok else response.text,
            status_ok=response.ok,
        )
