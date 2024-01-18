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

from hcs_core.sglib.client_util import hdc_service_client, default_crud, wait_for_res_status
from hcs_core.util.query_util import with_query, PageRequest

_client = hdc_service_client("admin")
_crud = default_crud(_client, "/v2/templates", "template")
get = _crud.get
list = _crud.list


def create(payload):
    return _crud.create(payload, ignore_warnings=True)


def delete(id: str, org_id: str, force: bool = True):
    return _crud.delete(id, org_id, force=force)


def wait_for_ready(id: str, org_id: str, timeout: str | int = "10m"):
    name = "template/" + id
    fn_get = lambda: get(id, org_id)
    fn_get_status = lambda t: t["reportedStatus"].get("statusValue")
    status_map = {
        "ready": "READY",
        "error": "ERROR",
        "transition": ["EXPANDING", "SHRINKING", "INIT"]
        # Unexpected:
        # DELETING
    }
    return wait_for_res_status(
        resource_name=name, fn_get=fn_get, get_status=fn_get_status, status_map=status_map, timeout=timeout
    )


wait_for_deleted = _crud.wait_for_deleted
