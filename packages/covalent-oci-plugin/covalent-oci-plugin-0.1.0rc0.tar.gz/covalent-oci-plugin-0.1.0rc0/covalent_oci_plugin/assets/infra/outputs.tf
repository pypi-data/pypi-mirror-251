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


# Outputs for public security list

output "security-list-name" {
  value = oci_core_security_list.public-security-list.display_name
}

output "security-list-id" {
  value = oci_core_security_list.public-security-list.id
}


# Outputs for the vcn module

output "vcn_id" {
  description = "OCID of the VCN that is created"
  value       = module.vcn.vcn_id
}

# output "id-for-route-table-that-includes-the-internet-gateway" {
#   description = "OCID of the internet-route table. This route table has an internet gateway to be used for public subnets"
#   value = module.vcn.ig_route_id
# }

# output "nat-gateway-id" {
#   description = "OCID for NAT gateway"
#   value = module.vcn.nat_gateway_id
# }

# output "id-for-for-route-table-that-includes-the-nat-gateway" {
#   description = "OCID of the nat-route table - This route table has a nat gateway to be used for private subnets. This route table also has a service gateway."
#   value = module.vcn.nat_route_id
# }


# Outputs for public subnet

output "subnet-name" {
  value = oci_core_subnet.vcn-public-subnet.display_name
}
output "subnet-id" {
  value = oci_core_subnet.vcn-public-subnet.id
}
