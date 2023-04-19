# Copyright 2023 SUSE LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Any, Dict, List, TypedDict

from pydantic import parse_obj_as

from backend.admin_ops import do_request
from backend.admin_ops.types import Bucket


class OptionalUIDParam(TypedDict, total=False):
    uid: str


class BucketListParams(OptionalUIDParam):
    stats: bool


async def list(
    url: str,
    access_key: str,
    secret_key: str,
    uid: str | None = None,
) -> List[Bucket]:
    """
    Obtains a list of `Bucket`, containing a multitude of information about each
    bucket available in the system. If `uid` is specified, returns only those
    buckets owned by the specified user id.
    """
    params: Dict[str, Any] = {"stats": True}
    if uid is not None and len(uid) > 0:
        params["uid"] = uid

    res = await do_request(
        url=url,
        access_key=access_key,
        secret_key=secret_key,
        endpoint="/admin/bucket",
        method="GET",
        params=params,
    )
    return parse_obj_as(List[Bucket], res.json())
