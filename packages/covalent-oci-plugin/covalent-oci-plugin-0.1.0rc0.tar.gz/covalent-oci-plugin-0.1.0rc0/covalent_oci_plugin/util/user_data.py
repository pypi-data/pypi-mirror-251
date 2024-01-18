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

# Include any dependencies for the plugin in this file.

import sys
from typing import Optional

USER_DATA_TEMPLATE = """\
#!/bin/bash

set -eu -o pipefail
export HOME=/home/{username}

__startup() {{
    sed -i '/^case \\$-.*/,+3d' /home/{username}/.bashrc
    cd $HOME

    MINICONDA_EXE="Miniconda3-py38_23.3.1-0-Linux-x86_64.sh"
    wget https://repo.anaconda.com/miniconda/$MINICONDA_EXE
    chmod +x $MINICONDA_EXE
    ./$MINICONDA_EXE -b -p $HOME/miniconda3
    rm $MINICONDA_EXE

    export PATH=$HOME/miniconda3/bin:$PATH
    eval "$(conda shell.bash hook)"
    conda init bash

    conda create -n covalent python={python_version} -y
    echo "conda activate covalent" >> $HOME/.bashrc

    chown -R {username}:{username} $HOME/{{.cache,.conda,miniconda3}}
    conda run -n covalent python -m pip install "covalent=={covalent_version}" "cloudpickle=={cloudpickle_version}"
    {optional_cuda_installation}
}}

(__startup && touch $HOME/setup_ready) > $HOME/covalent_setup.log 2>&1 || touch $HOME/setup_error
"""


def format_user_data(username: str, cuda_version: Optional[str] = None) -> str:
    """Format the setup shell script."""
    from cloudpickle import __version__ as cloudpickle_version
    from covalent import __version__ as covalent_version

    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    if cuda_version is None:
        cuda_install = ""  # skip installation
    elif cuda_version == "":
        cuda_install = 'conda run -n covalent conda install nvidia::cuda-toolkit -y'
    else:
        cuda_install = f'conda run -n covalent conda install nvidia/label/cuda-{cuda_version}::cuda-toolkit -y'

    return USER_DATA_TEMPLATE.format(
        username=username,
        python_version=python_version,
        covalent_version=covalent_version,
        cloudpickle_version=cloudpickle_version,
        optional_cuda_installation=cuda_install,
    )
