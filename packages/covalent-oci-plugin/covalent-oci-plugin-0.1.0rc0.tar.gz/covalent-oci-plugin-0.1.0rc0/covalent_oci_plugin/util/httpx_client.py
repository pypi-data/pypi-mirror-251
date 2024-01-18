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

"""Provides an HTTPX client for OCI API requests."""

from typing import Any, Dict, List

import httpx
from covalent._shared_files.logger import app_log
from oci.base_client import BaseClient
from oci.core.models import Instance, Vnic, VnicAttachment

from covalent_oci_plugin.util.httpx_auth import OCIHttpxAuth


class OCIHttpxClient(httpx.AsyncClient):
    """Adapts the OCI base client to httpx for asyncio."""

    _endpoints = {
        "LaunchInstance": "/20160918/instances",
        "ListVnicAttachments": "/20160918/vnicAttachments",
        "Vnic": "/20160918/vnics",
    }

    def __init__(
        self,
        config: Dict[str, Any],
        base_client: BaseClient,
        **kwargs: any,
    ):
        self.config = config
        self.base_client = base_client
        super().__init__(**kwargs)

    @property
    def api_base_url(self) -> str:
        """The base URL for the OCI API"""
        region = self.config["region"]
        return f"https://iaas.{region}.oraclecloud.com"

    async def launch_instance(self, details_json: str) -> Instance:
        """
        Launches an OCI Compute instance.

        Args:
            details_json: The JSON string containing the instance details.

        Returns:
            A model describing the newly launched OCI Compute instance.
        """
        auth = OCIHttpxAuth(self.config, enforce_content_headers=True)
        headers = auth.get_headers(details_json)

        app_log.debug("Launching instance with details: %s", details_json)
        response = await self.post(
            url=f"{self.api_base_url}{self._endpoints['LaunchInstance']}",
            headers=headers,
            data=details_json,
            auth=auth,
        )
        response.raise_for_status()

        return self.base_client.deserialize_response_data(
            response.content,
            "Instance",
        )

    async def terminate_instance(self, instance_id: str) -> None:
        """
        Terminates an OCI Compute instance.

        Args:
            instance_id: The OCID of the instance to terminate.
        """
        auth = OCIHttpxAuth(self.config, enforce_content_headers=False)
        headers = auth.get_headers()
        url = f"{self.api_base_url}{self._endpoints['LaunchInstance']}/{instance_id}"

        app_log.debug("Terminating instance '%s'", instance_id)
        response = await self.delete(url=url, headers=headers, auth=auth)
        response.raise_for_status()

    async def get_instance(self, instance_id: str) -> Instance:
        """
        Gets a description of an OCI Compute instance.

        Args:
            instance_id: The OCID of the instance to get.

        Returns:
            A model describing the newly launched OCI Compute instance.
        """

        auth = OCIHttpxAuth(self.config, enforce_content_headers=False)
        headers = auth.get_headers()
        url = f"{self.api_base_url}{self._endpoints['LaunchInstance']}/{instance_id}"

        response = await self.get(url=url, headers=headers, auth=auth)
        response.raise_for_status()

        return self.base_client.deserialize_response_data(
            response.content,
            "Instance",
        )

    async def get_vnic_attachments(self, compartment_id: str) -> List[VnicAttachment]:
        """
        Gets the list of VNIC attachments in a compartment.

        Args:
            compartment_id: The OCID of the compartment to get VNIC attachments from.

        Returns:
            A list of models describing the VNIC attachments in the compartment.
        """

        auth = OCIHttpxAuth(self.config, enforce_content_headers=False)
        headers = auth.get_headers()
        url = f"{self.api_base_url}{self._endpoints['ListVnicAttachments']}"

        response = await self.get(
            url=url,
            headers=headers,
            auth=auth,
            params={"compartmentId": compartment_id},
        )
        response.raise_for_status()

        return self.base_client.deserialize_response_data(
            response.content,
            "list[VnicAttachment]",
        )

    async def get_vnic(self, compartment_id: str, instance_id: str) -> Vnic:
        """
        Gets a description of the VNIC attached to the specified instance.

        Args:
            compartment_id: The OCID of the compartment to get VNIC attachments from.
            instance_id: The OCID of the instance to which the VNIC is attached.

        Returns:
            A model describing the VNIC attached to the specified instance.
        """

        instance_vnic_attachment = next(
            va for va in await self.get_vnic_attachments(compartment_id)
            if va.instance_id == instance_id
        )
        vnic_id = instance_vnic_attachment.vnic_id

        auth = OCIHttpxAuth(self.config, enforce_content_headers=False)
        headers = auth.get_headers()
        url = f"{self.api_base_url}{self._endpoints['Vnic']}/{vnic_id}"

        response = await self.get(url=url, headers=headers, auth=auth)
        response.raise_for_status()

        return self.base_client.deserialize_response_data(
            response.content,
            "Vnic",
        )

    async def get_instance_public_ip(
        self,
        compartment_id: str,
        instance_id: str
    ) -> str:
        """
        Gets the public IP address of an OCI Compute instance.

        Args:
            instance_id: The OCID of the instance to get the public IP address of.

        Returns:
            The public IP address of the instance.
        """
        vnic = await self.get_vnic(compartment_id, instance_id)
        return vnic.public_ip
