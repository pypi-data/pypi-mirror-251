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


class V1MeetingsMeetingIdGet200ResponseMeetingInfoListInnerSubMeetingsInner(object):
    """V1MeetingsMeetingIdGet200ResponseMeetingInfoListInnerSubMeetingsInner

    :param end_time:
    :type end_time: Optional[str]

    :param start_time:
    :type start_time: Optional[str]

    :param status:
    :type status: Optional[int]

    :param sub_meeting_id:
    :type sub_meeting_id: Optional[str]
    """  # noqa: E501

    end_time: Optional[str] = None
    start_time: Optional[str] = None
    status: Optional[int] = None
    sub_meeting_id: Optional[str] = None
    additional_properties: Dict[str, Any] = {}

    def __init__(
        self,
        end_time: Optional[str] = None,
        start_time: Optional[str] = None,
        status: Optional[int] = None,
        sub_meeting_id: Optional[str] = None,
        **kwargs
    ):
        self.end_time = end_time
        self.start_time = start_time
        self.status = status
        self.sub_meeting_id = sub_meeting_id

