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


class V1MeetingsMeetingIdEnrollConfigPut200Response(object):
    """V1MeetingsMeetingIdEnrollConfigPut200Response

    :param meeting_id: 会议的唯一标识 
    :type meeting_id: Optional[str]

    :param question_count: 报名问题数量，不收集问题时该字段返回0 
    :type question_count: Optional[int]
    """  # noqa: E501

    meeting_id: Optional[str] = None
    question_count: Optional[int] = None
    additional_properties: Dict[str, Any] = {}

    def __init__(
        self,
        meeting_id: Optional[str] = None,
        question_count: Optional[int] = None,
        **kwargs
    ):
        self.meeting_id = meeting_id
        self.question_count = question_count

