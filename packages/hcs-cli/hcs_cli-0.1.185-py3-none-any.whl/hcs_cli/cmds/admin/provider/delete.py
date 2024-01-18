"""
Copyright 2023-2023 VMware Inc.
SPDX-License-Identifier: Apache-2.0

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import click
from hcs_cli.service import admin
import hcs_core.sglib.cli_options as cli


@click.command()
@click.argument("id", type=str, required=True)
@click.option("--label", type=str, required=False, default="azure")
@cli.org_id
def delete(label: str, id: str, org: str):
    """Delete provider by ID"""
    ret = admin.provider.delete(label, id, org_id=cli.get_org_id(org), force=True)
    if ret:
        return ""
    return "", 1
