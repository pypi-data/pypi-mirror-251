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


class V1MeetingsGet200ResponseMeetingInfoListInnerGuestsInner(object):
    """V1MeetingsGet200ResponseMeetingInfoListInnerGuestsInner

    :param area:
    :type area: Optional[str]

    :param guest_name:
    :type guest_name: Optional[str]

    :param phone_number:
    :type phone_number: Optional[str]
    """  # noqa: E501

    area: Optional[str] = None
    guest_name: Optional[str] = None
    phone_number: Optional[str] = None
    additional_properties: Dict[str, Any] = {}

    def __init__(
        self,
        area: Optional[str] = None,
        guest_name: Optional[str] = None,
        phone_number: Optional[str] = None,
        **kwargs
    ):
        self.area = area
        self.guest_name = guest_name
        self.phone_number = phone_number

