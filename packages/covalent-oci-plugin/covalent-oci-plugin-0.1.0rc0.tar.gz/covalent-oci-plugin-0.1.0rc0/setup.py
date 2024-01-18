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

import site
import sys

from setuptools import find_packages, setup

site.ENABLE_USER_SITE = "--user" in sys.argv[1:]

with open("VERSION", encoding="utf-8") as f:
    version = f.read().strip()

with open("requirements.txt", encoding="utf-8") as f:
    required = f.read().splitlines()

plugins_list = [
    "oci = covalent_oci_plugin.oci"
]

setup_info = {
    # Your plugin should use the naming convention 'covalent-abcdef-plugin'
    "name": "covalent-oci-plugin",
    "packages": find_packages("."),
    "version": version,
    # Modify any contact information as you see fit
    "maintainer": "Agnostiq",
    "url": "https://github.com/AgnostiqHQ/covalent-oci-plugin",
    "download_url": f"https://github.com/AgnostiqHQ/covalent-oci-plugin/archive/v{version}.tar.gz",
    "license": "Apache License 2.0",
    "author": "Agnostiq",
    "author_email": "support@agnostiq.ai",
    "description": "Covalent OCI Plugin",
    "long_description": open("README.md", encoding="utf-8").read(),
    "long_description_content_type": "text/markdown",
    "include_package_data": True,
    "install_requires": required,
    "classifiers": [
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Adaptive Technologies",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
        "Topic :: Software Development",
        "Topic :: System :: Distributed Computing",
    ],
    "entry_points": {
        "covalent.executor.executor_plugins": plugins_list,
    },
}

if __name__ == "__main__":
    setup(**setup_info)
