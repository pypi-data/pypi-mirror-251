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


class V1MeetingsMeetingIdEnrollIdsPost200ResponseEnrollIdListInner(object):
    """V1MeetingsMeetingIdEnrollIdsPost200ResponseEnrollIdListInner

    :param enroll_id: 报名ID 
    :type enroll_id: Optional[int]

    :param ms_open_id: 当场会议的用户临时 ID，适用于所有用户。 
    :type ms_open_id: Optional[str]
    """  # noqa: E501

    enroll_id: Optional[int] = None
    ms_open_id: Optional[str] = None
    additional_properties: Dict[str, Any] = {}

    def __init__(
        self,
        enroll_id: Optional[int] = None,
        ms_open_id: Optional[str] = None,
        **kwargs
    ):
        self.enroll_id = enroll_id
        self.ms_open_id = ms_open_id

