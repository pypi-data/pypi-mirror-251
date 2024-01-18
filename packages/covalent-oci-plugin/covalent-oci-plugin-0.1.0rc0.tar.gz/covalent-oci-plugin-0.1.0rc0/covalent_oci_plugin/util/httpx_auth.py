# Copyright 2024 Agnostiq Inc.
#
# This file is part of Covalent.
#
# Licensed under the Apache License 2.0 (the "License"). A copy of the
# License may be obtained with this software package or at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Use of this file is prohibited except in compliance with the License.
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Implement a custom auth class for OCI requests via httpx"""

import base64
import email.utils
import hashlib
from typing import Any, Dict

import httpx
from oci.signer import Signer


class OCIHttpxAuth(httpx.Auth):
    """Adapts the OCI Signer to httpx."""

    def __init__(
        self,
        config: Dict[str, Any],
        *,
        enforce_content_headers: bool,
    ):
        """
        Create and auth object.

        Args:
            config: The OCI config dictionary
            enforce_content_headers: Whether to enforce content headers
        """
        self.config = config
        self.enforce_content_headers = enforce_content_headers

    def auth_flow(self, request: httpx.Request) -> httpx.Request:
        signed_request = self.sign_request(request)
        yield signed_request

    def sign_request(self, request: httpx.Request) -> httpx.Request:
        """
        Sign the request (i.e use the OCI signer to sign the request).

        Returns:
            httpx.Request: The signed request object
        """
        if self.enforce_content_headers:
            signer = Signer.from_config(self.config)._body_signer
        else:
            signer = Signer.from_config(self.config)._basic_signer

        signature = signer.sign(
            host=request.url.host,
            method=request.method,
            headers=request.headers,
            path=(
                request.url.path if not request.url.params
                else f"{request.url.path}?{request.url.query.decode()}"
            ),
        )
        request.headers["Authorization"] = signature["authorization"]

        return request

    def get_headers(self, body: str = "") -> Dict[str, Any]:
        """
        Get the headers for the request from the body of the request.

        Args:
            body: JSON string of the request body

        Returns:
            Dict[str, Any]: The headers for the request
        """
        headers = {
            "content-type": "application/json",
            "accept": "application/json",
            "date": email.utils.formatdate(usegmt=True)
        }
        if self.enforce_content_headers:
            headers.update({
                "content-length": str(len(body.encode())),
                "x-content-sha256": self.content_sha256_base64(body),
            })
        return headers

    @staticmethod
    def content_sha256_base64(body: str) -> str:
        """
        Get the SHA256 hash of the request body.

        Args:
            body: JSON string of the request body

        Returns:
            str: The SHA256 hash of the request body
        """
        content_hash = hashlib.sha256(body.encode("utf-8")).digest()
        return base64.b64encode(content_hash).decode("utf-8")
