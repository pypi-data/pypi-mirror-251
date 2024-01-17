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


class V1MeetingsMeetingIdPut200ResponseMeetingInfoListInnerLiveConfig(object):
    """直播配置对象，内部只返回 live_addr（直播观看地址）。

    :param live_addr: 直播观看地址 
    :type live_addr: Optional[str]
    """  # noqa: E501

    live_addr: Optional[str] = None
    additional_properties: Dict[str, Any] = {}

    def __init__(
        self,
        live_addr: Optional[str] = None,
        **kwargs
    ):
        self.live_addr = live_addr

