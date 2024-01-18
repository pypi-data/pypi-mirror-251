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

"""Implements the Covalent Oracle Cloud Infrastructure (OCI) Executor"""

# Please don't rename this module to 'oci.py' as it will conflict with the OCI SDK.

import asyncio
import base64
import json
from copy import deepcopy
from enum import Enum, auto
from pathlib import Path
from typing import Any, Dict, Optional, List

import httpx
import oci
from covalent._shared_files.config import get_config
from covalent._shared_files.logger import app_log
from covalent_ssh_plugin.ssh import _EXECUTOR_PLUGIN_DEFAULTS as _SSH_EXECUTOR_PLUGIN_DEFAULTS
from covalent_ssh_plugin.ssh import SSHExecutor
from oci.base_client import BaseClient
from oci.core.compute_client import ComputeClient
from oci.core.models import (
    CreateVnicDetails,
    Instance,
    InstanceSourceViaImageDetails,
    LaunchInstanceDetails,
)
from pydantic import BaseModel

from covalent_oci_plugin.util.httpx_client import OCIHttpxClient
from covalent_oci_plugin.util.misc import matching_public_key
from covalent_oci_plugin.util.user_data import format_user_data


class ExecutorPluginDefaults(BaseModel):
    """Default values for the OCI Executor"""
    # SSHExecutor
    username: str = "ubuntu"
    hostname: str = ""
    ssh_key_file: str = str(Path.home() / ".oci/id_rsa")
    cache_dir: str = ""
    python_path: str = ""
    conda_env: str = ""
    remote_cache: str = ""
    run_local_on_ssh_fail: bool = False
    remote_workdir: str = ""
    create_unique_workdir: bool = False

    # OCIExecutor
    shape: str = ""
    image_id: str = ""
    availability_domain: str = ""
    compartment_id: str = ""
    subnet_id: str = ""
    region: str = "us-ashburn-1"
    oci_config_file: str = str(Path.home() / ".oci/config")
    boot_volume_size_in_gbs: int = 214
    ssh_key_file_public: str = ""
    cuda_version: Optional[str] = None


# TODO: These values are not being propagated to the terraform code, will need to fix it
class ExecutorInfraDefaults(BaseModel):
    """Default values for the infra deployment of OCI Plugin"""

    prefix: str = "covalent"

    # For terraform oci provider
    tenancy_ocid: str = ""
    compartment_ocid: str
    user_ocid: str = ""
    private_key_path: str = ""
    fingerprint: str = ""
    region: str = ""
    config_file_profile: str = ""

    # For networking
    cidr_block: str = ""
    allowed_ips: List[str] = []  # TODO: implement adding these in the terraform code


_EXECUTOR_PLUGIN_DEFAULTS = deepcopy(_SSH_EXECUTOR_PLUGIN_DEFAULTS)
_EXECUTOR_PLUGIN_DEFAULTS.update(ExecutorPluginDefaults().model_dump())


class InstanceLifecycleState(Enum):
    """Instance lifecycle states"""
    MOVING = auto()
    PROVISIONING = auto()
    RUNNING = auto()
    STARTING = auto()
    STOPPING = auto()
    STOPPED = auto()
    CREATING_IMAGE = auto()
    TERMINATING = auto()
    TERMINATED = auto()


class OCIExecutor(SSHExecutor):
    """Covalent Oracle Cloud Infrastructure (OCI) Executor"""

    # TODO: double check required versus optional params for instances API
    # TODO: explore using instance configurations to auto set up key pair

    def __init__(
        self,
        shape: str,
        availability_domain: str,
        image_id: str,
        compartment_id: str,
        subnet_id: str,
        region: Optional[str] = None,
        oci_config_file: Optional[str] = None,
        boot_volume_size_in_gbs: Optional[int] = None,
        ssh_key_file_public: Optional[str] = None,
        cuda_version: Optional[str] = None,
        **kwargs: Any,
    ):
        """
        Initialize the OCI Executor.

        Args:
            shape: The shape of the instance to launch, e.g. 'VM.Standard.E2.1'
            image_id: The OCID of the image to use for the instance
            availability_domain: The availability domain to launch the instance in, e.g. 'giLp:US-ASHBURN-AD-1'
            compartment_id: The OCID of the compartment to launch the instance in
            subnet_id: The OCID of the subnet to launch the instance in
            region: The region to launch the instance in, e.g. 'us-ashburn-1'
            oci_config_file: The path to the OCI config file, defaults to '~/.oci/config'
            boot_volume_size_in_gbs: The size of the boot volume in GBs
            ssh_key_file_public: The path to the SSH public key file, defaults to '<ssh_key_file>.pub'
            cuda_version: Specify CUDA version (e.g. '11.3.1') to install on the instance.
                          Specify the empty string ('') to install the latest version.
                          No CUDA is installed when `cuda_version` is None, by default.

            **kwargs: Additional keyword arguments to pass to the SSHExecutor

        """

        self.shape = (
            shape
            or get_config("executors.oci.shape")
        )
        self.image_id = (
            image_id
            or get_config("executors.oci.image_id")
        )
        self.availability_domain = (
            availability_domain
            or get_config("executors.oci.availability_domain")
        )
        self.compartment_id = (
            compartment_id
            or get_config("executors.oci.compartment_id")
        )
        self.subnet_id = (
            subnet_id
            or get_config("executors.oci.subnet_id")
        )
        self.region = (
            region
            or get_config("executors.oci.region")
        )
        self.oci_config_file = (
            oci_config_file
            or get_config("executors.oci.oci_config_file")
        )
        self.boot_volume_size_in_gbs = (
            boot_volume_size_in_gbs
            or get_config("executors.oci.boot_volume_size_in_gbs")
        )
        self.ssh_key_file_public = (
            ssh_key_file_public
            or get_config("executors.oci.ssh_key_file_public")
        )
        self.cuda_version = (
            cuda_version
            or get_config("executors.oci.cuda_version")
        )

        if (retry_wait_time := kwargs.get("retry_wait_time")):
            # Setting lower limit gives SSH service time to start up.
            retry_wait_time = 20 if retry_wait_time < 20 else retry_wait_time
        else:
            retry_wait_time = 20

        kwargs.update(
            hostname="",
            username=kwargs.get("username", get_config("executors.oci.username")),
            ssh_key_file=kwargs.get("ssh_key_file", get_config("executors.oci.ssh_key_file")),
            retry_wait_time=retry_wait_time,
        )
        super().__init__(**kwargs)

        # Initialize private attributes.
        self._config: Dict[str, Any] = None
        self._compute_client: ComputeClient = None
        self._instance: Instance = None

    def _validate_before_setup(self) -> None:
        if not self.ssh_key_file:
            raise ValueError("executor's `ssh_key_file` is not set")
        if self.poll_freq and self.poll_freq < 0:
            raise ValueError("executor's `poll_freq` is not a positive integer")
        if not self.username:
            raise ValueError("executor's `username` is not set")

    @property
    def config(self) -> Dict[str, Any]:
        """Validated dictionary that holds th OCI config."""
        if self._config is None:
            self._config = oci.config.from_file(file_location=self.oci_config_file)
            oci.config.validate_config(self._config)

        return self._config

    @property
    def compute_client(self) -> ComputeClient:
        """Lazy-loaded OCI ComputeClient."""
        if self._compute_client is None:
            self._compute_client = ComputeClient(self.config)
        return self._compute_client

    @property
    def base_client(self) -> BaseClient:
        """Lazy-loaded OCI BaseClient."""
        return self.compute_client.base_client

    @property
    def instance(self) -> Instance:
        """Holds the model of an OCI Compute instance."""
        return self._instance

    @instance.setter
    def instance(self, instance: Instance) -> None:
        """Update the model of an OCI Compute instance."""
        if self._instance is not None and self._instance.id != instance.id:
            raise ValueError(
                f"Cannot update current instance (OCID {self._instance.id}) "
                f"with a different instance (OCID {instance.id}))"
            )
        self._instance = instance

    def _read_public_key(self) -> str:
        """The public key to use for SSH authentication."""
        if self.ssh_key_file_public:
            ssh_key_file_public = Path(self.ssh_key_file_public).expanduser()
        else:
            ssh_key_file_public = self._locate_public_key_file()

        return ssh_key_file_public.read_text("utf-8")

    def _locate_public_key_file(self) -> Path:
        """Attempt to locate a public key matching the private key."""
        if not (key_file_match := matching_public_key(self.ssh_key_file)):
            raise ValueError(
                "Unable to auto-locate public key, please specify `ssh_key_file_public` "
                "or rename your keys to match one another."
            )
        return Path(key_file_match).expanduser()

    def _sanitize_instance(self, instance: Instance) -> Dict[str, Any]:
        """Removes null values and format keys for serialization."""
        return self.base_client.sanitize_for_serialization(instance)

    def _override_model_fields(self, model: Any, *field_names: str) -> Any:
        """
        Helper that preserves default values for OCI model fields, unless
        corresponding user parameters are truthy.
        """
        for field in field_names:
            if value := getattr(self, field):
                # Only override with truthy attributes values.
                setattr(model, field, value)

        return model

    def _encode_user_data(self) -> str:
        """Encode the user data to base64."""
        user_data = format_user_data(self.username, self.cuda_version)
        app_log.debug("Setup script:\n%s", user_data)
        return base64.b64encode(user_data.encode("utf-8")).decode("utf-8")

    def _build_launch_instance_details(
        self,
        dispatch_id: str,
        node_id: str
    ) -> Dict[str, Any]:
        """Use OCI model for instance launch details to build the request body."""
        source_details = self._override_model_fields(
            InstanceSourceViaImageDetails(
                source_type="image"
            ),
            "boot_volume_size_in_gbs",
            "image_id",
        )
        create_vnic_details = self._override_model_fields(
            CreateVnicDetails(
                display_name=f"vnic-{dispatch_id}-{node_id}",
                assign_public_ip=True,
            ),
            "subnet_id",
        )
        launch_instance_details = self._override_model_fields(
            LaunchInstanceDetails(
                display_name=f"instance-{dispatch_id}-{node_id}",
                availability_domain=self.availability_domain,
                shape=self.shape,
                source_details=source_details,
                create_vnic_details=create_vnic_details,
                metadata={
                    "ssh_authorized_keys": self._read_public_key(),
                    "user_data": self._encode_user_data(),
                }
            ),
            "compartment_id",
        )

        return self._sanitize_instance(launch_instance_details)

    async def _poll_instance_until_state(
        self,
        lifecycle_state: InstanceLifecycleState,
        client: httpx.AsyncClient,
    ) -> None:
        """Poll the instance state until it reaches the desired state."""

        # Poll for up to 1 hour.
        t = 5
        max_iteration = 3600 // t
        iteration = 0

        while iteration < max_iteration:
            app_log.debug(
                "Polling instance '%s' - state '%s' - waiting for state '%s'",
                self.instance.id, self.instance.lifecycle_state, lifecycle_state.name
            )
            try:
                self.instance = await client.get_instance(self.instance.id)
            except httpx.HTTPStatusError as e:
                raise RuntimeError(e) from e

            if self.instance.lifecycle_state != lifecycle_state.name:
                await asyncio.sleep(t)
                iteration += 1
            else:
                app_log.debug(
                    "Polling instance '%s' - done after %d seconds! Confirmed state '%s'",
                    self.instance.id, iteration * t, lifecycle_state.name
                )
                break  # Done polling.

        if not iteration < max_iteration:
            raise RuntimeError(
                f"Timeout while polling instance '{self.instance.id}' "
                f"for state '{lifecycle_state.name}'"
            )

    async def _prepare_instance_to_run_task(self, client: OCIHttpxClient) -> None:
        """Prepare a launched instance to run the electron task."""

        self.hostname = await client.get_instance_public_ip(
            self.compartment_id, self.instance.id
        )
        app_log.debug("Connecting to %s", f"{self.username}@{self.hostname}")
        ssh_success, conn = await self._client_connect()

        if not ssh_success:
            raise RuntimeError(f"Failed to connect to remote {self.hostname}")

        app_log.debug("Waiting for setup script to finish on %s ", self.hostname)
        while (await conn.run("[ -e setup_ready ]")).returncode != 0:

            # Exit when certain that setup failed.
            if (await conn.run("[ -e setup_error ]")).returncode == 0:
                raise RuntimeError(f"Detected setup failure on remote {self.hostname} with error:\n {(await conn.run('tail -n 50 covalent_setup.log')).stdout}")

            await asyncio.sleep(self.poll_freq or 5)

        conn.close()
        await conn.wait_closed()

    async def setup(self, task_metadata: Dict[str, Any]) -> None:

        self._validate_before_setup()
        dispatch_id = task_metadata["dispatch_id"]
        node_id = task_metadata["node_id"]
        app_log.debug("Setup - Dispatch %s Node %s - started", dispatch_id, node_id)

        # Obtain launch instance details, i.e. request body.
        launch_instance_details_json = json.dumps(
            self._build_launch_instance_details(dispatch_id, node_id)
        )
        async with OCIHttpxClient(self.config, self.base_client) as client:
            try:
                self.instance = await client.launch_instance(launch_instance_details_json)
            except httpx.HTTPStatusError as e:
                raise RuntimeError(e) from e

            # Wait until the instance is up and running.
            await self._poll_instance_until_state(InstanceLifecycleState.RUNNING, client)

            app_log.debug("Setup - Dispatch %s Node %s - preparing...", dispatch_id, node_id)

            # Proceed with software setup.
            await self._prepare_instance_to_run_task(client)

        app_log.debug(
            "Setup - Dispatch %s Node %s - done! Created instance '%s'",
            dispatch_id, node_id, self.instance.id
        )

    async def teardown(self, task_metadata: Dict[str, Any]) -> None:

        dispatch_id = task_metadata["dispatch_id"]
        node_id = task_metadata["node_id"]
        app_log.debug("Requesting teardown - Dispatch %s Node %s", dispatch_id, node_id)

        if self.instance:
            async with OCIHttpxClient(self.config, self.base_client) as client:
                try:
                    await client.terminate_instance(self.instance.id)
                except httpx.HTTPStatusError as e:
                    raise RuntimeError(e) from e

                # await self._poll_instance_until_state(InstanceLifecycleState.TERMINATED, client)
        else:
            app_log.error("No instance to terminate - Dispatch %s Node %s", dispatch_id, node_id)


EXECUTOR_PLUGIN_NAME = OCIExecutor.__name__
