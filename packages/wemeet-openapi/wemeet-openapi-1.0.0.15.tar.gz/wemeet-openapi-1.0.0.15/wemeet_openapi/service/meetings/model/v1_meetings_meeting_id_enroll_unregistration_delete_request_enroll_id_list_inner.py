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


class V1MeetingsMeetingIdEnrollUnregistrationDeleteRequestEnrollIdListInner(object):
    """V1MeetingsMeetingIdEnrollUnregistrationDeleteRequestEnrollIdListInner

    :param enroll_id: 报名ID (required) 
    :type enroll_id: int
    """  # noqa: E501

    enroll_id: int
    additional_properties: Dict[str, Any] = {}

    def __init__(
        self,
        enroll_id: int,
        **kwargs
    ):
        self.enroll_id = enroll_id

