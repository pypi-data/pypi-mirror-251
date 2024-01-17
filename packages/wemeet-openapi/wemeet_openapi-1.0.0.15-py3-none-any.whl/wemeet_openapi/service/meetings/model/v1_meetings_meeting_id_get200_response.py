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
from wemeet_openapi.service.meetings.model.v1_meetings_meeting_id_get200_response_meeting_info_list_inner import V1MeetingsMeetingIdGet200ResponseMeetingInfoListInner


class V1MeetingsMeetingIdGet200Response(object):
    """V1MeetingsMeetingIdGet200Response

    :param meeting_info_list:
    :type meeting_info_list: Optional[List[V1MeetingsMeetingIdGet200ResponseMeetingInfoListInner]]

    :param meeting_number:
    :type meeting_number: Optional[int]
    """  # noqa: E501

    meeting_info_list: Optional[List[V1MeetingsMeetingIdGet200ResponseMeetingInfoListInner]] = None
    meeting_number: Optional[int] = None
    additional_properties: Dict[str, Any] = {}

    def __init__(
        self,
        meeting_info_list: Optional[List[V1MeetingsMeetingIdGet200ResponseMeetingInfoListInner] | List[Dict[str, Any]]] = None,
        meeting_number: Optional[int] = None,
        **kwargs
    ):
        
        if meeting_info_list and isinstance(meeting_info_list, (list, List)):
            self.meeting_info_list = [V1MeetingsMeetingIdGet200ResponseMeetingInfoListInner(**_item) if isinstance(_item, (dict, Dict)) else _item for _item in meeting_info_list]
        
        self.meeting_number = meeting_number

