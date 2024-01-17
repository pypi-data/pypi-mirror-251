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


class V1MeetingsPostRequestGuestsInner(object):
    """V1MeetingsPostRequestGuestsInner

    :param area: 国家/地区代码（例如：中国传86，不是+86，也不是0086） (required) 
    :type area: str

    :param guest_name: 嘉宾名称 
    :type guest_name: Optional[str]

    :param phone_number: 手机号 (required) 
    :type phone_number: str
    """  # noqa: E501

    area: str
    guest_name: Optional[str] = None
    phone_number: str
    additional_properties: Dict[str, Any] = {}

    def __init__(
        self,
        area: str,
        phone_number: str,
        guest_name: Optional[str] = None,
        **kwargs
    ):
        self.area = area
        self.guest_name = guest_name
        self.phone_number = phone_number

