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


class V1MeetingsPost200ResponseMeetingInfoListInnerHostsInner(object):
    """V1MeetingsPost200ResponseMeetingInfoListInnerHostsInner

    :param userid:
    :type userid: Optional[str]
    """  # noqa: E501

    userid: Optional[str] = None
    additional_properties: Dict[str, Any] = {}

    def __init__(
        self,
        userid: Optional[str] = None,
        **kwargs
    ):
        self.userid = userid

