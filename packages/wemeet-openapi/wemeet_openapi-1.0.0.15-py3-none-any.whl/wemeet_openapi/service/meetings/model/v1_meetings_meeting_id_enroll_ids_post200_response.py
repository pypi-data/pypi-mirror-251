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
from wemeet_openapi.service.meetings.model.v1_meetings_meeting_id_enroll_ids_post200_response_enroll_id_list_inner import V1MeetingsMeetingIdEnrollIdsPost200ResponseEnrollIdListInner


class V1MeetingsMeetingIdEnrollIdsPost200Response(object):
    """V1MeetingsMeetingIdEnrollIdsPost200Response

    :param enroll_id_list: 成员报名 ID 数组，仅返回已报名成员的报名 ID，若传入的用户无人报名，则无该字段。 
    :type enroll_id_list: Optional[List[V1MeetingsMeetingIdEnrollIdsPost200ResponseEnrollIdListInner]]

    :param meeting_id: 会议ID 
    :type meeting_id: Optional[str]
    """  # noqa: E501

    enroll_id_list: Optional[List[V1MeetingsMeetingIdEnrollIdsPost200ResponseEnrollIdListInner]] = None
    meeting_id: Optional[str] = None
    additional_properties: Dict[str, Any] = {}

    def __init__(
        self,
        enroll_id_list: Optional[List[V1MeetingsMeetingIdEnrollIdsPost200ResponseEnrollIdListInner] | List[Dict[str, Any]]] = None,
        meeting_id: Optional[str] = None,
        **kwargs
    ):
        
        if enroll_id_list and isinstance(enroll_id_list, (list, List)):
            self.enroll_id_list = [V1MeetingsMeetingIdEnrollIdsPost200ResponseEnrollIdListInner(**_item) if isinstance(_item, (dict, Dict)) else _item for _item in enroll_id_list]
        
        self.meeting_id = meeting_id

