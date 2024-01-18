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

import covalent as ct
import pytest


@pytest.mark.functional_tests
def test_workflow():
    oci = ct.executor.OCIExecutor(
        availability_domain="giLp:US-ASHBURN-AD-1",
        shape="VM.Standard.E2.1",
        compartment_id="ocid1.compartment.oc1..unique-compartment-id",
        image_id="ocid1.image.oc1.iad.unique-image-id",
        subnet_id="ocid1.subnet.oc1.iad.unique-subnet-id",
        # ssh_key_file="~/.oci/id_rsa",
    )

    @ct.electron(executor=oci, deps_pip=["art==6.1"])
    def create_title(text: str):
        from art import text2art
        return text2art(text)

    @ct.lattice
    def workflow(text: str):
        return create_title(text)

    dispatch_id = ct.dispatch(workflow)("Oracle Compute Infrastructure")
    print(f"Dispatch ID: {dispatch_id}")

    # result = ct.get_result(dispatch_id, wait=True)
    # print(f"Result: {result}")
