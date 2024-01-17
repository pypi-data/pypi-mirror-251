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


class V1MeetingsGet200ResponseMeetingInfoListInnerCurrentCoHostsInner(object):
    """V1MeetingsGet200ResponseMeetingInfoListInnerCurrentCoHostsInner

    :param userid:
    :type userid: Optional[str]

    :param userid_type: userid类型，1：userid 2：openid 3：rooms_id 4：ms_open_id 
    :type userid_type: Optional[int]
    """  # noqa: E501

    userid: Optional[str] = None
    userid_type: Optional[int] = None
    additional_properties: Dict[str, Any] = {}

    def __init__(
        self,
        userid: Optional[str] = None,
        userid_type: Optional[int] = None,
        **kwargs
    ):
        self.userid = userid
        self.userid_type = userid_type

