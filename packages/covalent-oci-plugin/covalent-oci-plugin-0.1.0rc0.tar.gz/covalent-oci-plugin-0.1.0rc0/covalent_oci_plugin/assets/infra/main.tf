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


provider "oci" {
  tenancy_ocid        = var.tenancy_ocid
  user_ocid           = var.user_ocid
  private_key_path    = var.private_key_path
  fingerprint         = var.fingerprint
  region              = var.region
  config_file_profile = var.config_file_profile
}

locals {
  compartment_ocid = var.compartment_ocid == "" ? var.tenancy_ocid : var.compartment_ocid
}


module "vcn" {
  source         = "oracle-terraform-modules/vcn/oci"
  version        = "~> 3.6"
  compartment_id = local.compartment_ocid

  vcn_name      = "${var.prefix}-vcn-module"
  vcn_dns_label = "${var.prefix}dns"
  vcn_cidrs     = [var.cidr_block]

  create_internet_gateway = true
  create_nat_gateway      = true
  create_service_gateway  = true
}


# Source from https://registry.terraform.io/providers/oracle/oci/latest/docs/resources/core_security_list

resource "oci_core_security_list" "public-security-list" {

  # Required
  compartment_id = local.compartment_ocid
  vcn_id         = module.vcn.vcn_id

  # Optional
  display_name = "${var.prefix}-security-list-for-public-subnet"

  egress_security_rules {
    stateless        = false
    destination      = "0.0.0.0/0"
    destination_type = "CIDR_BLOCK"
    protocol         = "all"
  }

  ingress_security_rules {
    stateless   = false
    source      = "0.0.0.0/0"
    source_type = "CIDR_BLOCK"
    # Get protocol numbers from https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml TCP is 6
    protocol = "6"
    tcp_options {
      min = 22
      max = 22
    }
  }
  ingress_security_rules {
    stateless   = false
    source      = "0.0.0.0/0"
    source_type = "CIDR_BLOCK"
    # Get protocol numbers from https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml ICMP is 1  
    protocol = "1"

    # For ICMP type and code see: https://www.iana.org/assignments/icmp-parameters/icmp-parameters.xhtml
    icmp_options {
      type = 3
      code = 4
    }
  }

  ingress_security_rules {
    stateless   = false
    source      = "10.0.0.0/16"
    source_type = "CIDR_BLOCK"
    # Get protocol numbers from https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml ICMP is 1  
    protocol = "1"

    # For ICMP type and code see: https://www.iana.org/assignments/icmp-parameters/icmp-parameters.xhtml
    icmp_options {
      type = 3
    }
  }

}


# Source from https://registry.terraform.io/providers/oracle/oci/latest/docs/resources/core_subnet

resource "oci_core_subnet" "vcn-public-subnet" {

  # Required
  compartment_id = local.compartment_ocid
  vcn_id         = module.vcn.vcn_id
  cidr_block     = "10.0.0.0/24"

  # Optional
  route_table_id    = module.vcn.ig_route_id
  security_list_ids = [oci_core_security_list.public-security-list.id]
  display_name      = "${var.prefix}-public-subnet"
}
