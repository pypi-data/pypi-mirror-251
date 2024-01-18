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


def list(template_id: str, **kwargs):
    def _get_page(query_string):
        url = f"/v2/templates/{template_id}/vms?" + query_string
        return _client.get(url)

    return PageRequest(_get_page, **kwargs).get()


def get(template_id: str, vm_id: str, **kwargs):
    url = with_query(f"/v2/templates/{template_id}/vms/{vm_id}", **kwargs)
    return _client.get(url)
