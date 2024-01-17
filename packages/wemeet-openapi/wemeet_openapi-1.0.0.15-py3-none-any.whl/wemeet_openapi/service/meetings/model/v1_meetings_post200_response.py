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
from wemeet_openapi.service.meetings.model.v1_meetings_post200_response_meeting_info_list_inner import V1MeetingsPost200ResponseMeetingInfoListInner


class V1MeetingsPost200Response(object):
    """V1MeetingsPost200Response

    :param meeting_info_list: 会议对象数组 
    :type meeting_info_list: Optional[List[V1MeetingsPost200ResponseMeetingInfoListInner]]

    :param meeting_number: 会议数量 
    :type meeting_number: Optional[int]
    """  # noqa: E501

    meeting_info_list: Optional[List[V1MeetingsPost200ResponseMeetingInfoListInner]] = None
    meeting_number: Optional[int] = None
    additional_properties: Dict[str, Any] = {}

    def __init__(
        self,
        meeting_info_list: Optional[List[V1MeetingsPost200ResponseMeetingInfoListInner] | List[Dict[str, Any]]] = None,
        meeting_number: Optional[int] = None,
        **kwargs
    ):
        
        if meeting_info_list and isinstance(meeting_info_list, (list, List)):
            self.meeting_info_list = [V1MeetingsPost200ResponseMeetingInfoListInner(**_item) if isinstance(_item, (dict, Dict)) else _item for _item in meeting_info_list]
        
        self.meeting_number = meeting_number

