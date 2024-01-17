# coding: utf-8

"""
    腾讯会议OpenAPI

    SAAS版RESTFUL风格API

    API version: v1.0.0.15

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations

from typing import *

# import models into model package


class V1MeetingsMeetingIdEnrollUnregistrationDelete200Response(object):
    """V1MeetingsMeetingIdEnrollUnregistrationDelete200Response

    :param total_count: 成功删除的报名信息数量 
    :type total_count: Optional[int]
    """  # noqa: E501

    total_count: Optional[int] = None
    additional_properties: Dict[str, Any] = {}

    def __init__(
        self,
        total_count: Optional[int] = None,
        **kwargs
    ):
        self.total_count = total_count

