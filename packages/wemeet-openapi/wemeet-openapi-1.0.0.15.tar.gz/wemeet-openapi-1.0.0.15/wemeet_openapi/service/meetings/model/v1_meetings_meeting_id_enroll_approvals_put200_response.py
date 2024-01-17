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


class V1MeetingsMeetingIdEnrollApprovalsPut200Response(object):
    """V1MeetingsMeetingIdEnrollApprovalsPut200Response

    :param handled_count: 成功处理的数量 
    :type handled_count: Optional[int]

    :param meeting_id: 在线大会唯一标识 
    :type meeting_id: Optional[str]
    """  # noqa: E501

    handled_count: Optional[int] = None
    meeting_id: Optional[str] = None
    additional_properties: Dict[str, Any] = {}

    def __init__(
        self,
        handled_count: Optional[int] = None,
        meeting_id: Optional[str] = None,
        **kwargs
    ):
        self.handled_count = handled_count
        self.meeting_id = meeting_id

