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
from wemeet_openapi.service.meetings.model.v1_meetings_meeting_id_enroll_import_post200_response_enroll_list_inner import V1MeetingsMeetingIdEnrollImportPost200ResponseEnrollListInner


class V1MeetingsMeetingIdEnrollImportPost200Response(object):
    """V1MeetingsMeetingIdEnrollImportPost200Response

    :param enroll_list: 报名对象列表  
    :type enroll_list: Optional[List[V1MeetingsMeetingIdEnrollImportPost200ResponseEnrollListInner]]

    :param total_count: 成功导入的报名信息条数 
    :type total_count: Optional[int]

    :param user_non_registered: 未注册用户列表 
    :type user_non_registered: Optional[List[str]]
    """  # noqa: E501

    enroll_list: Optional[List[V1MeetingsMeetingIdEnrollImportPost200ResponseEnrollListInner]] = None
    total_count: Optional[int] = None
    user_non_registered: Optional[List[str]] = None
    additional_properties: Dict[str, Any] = {}

    def __init__(
        self,
        enroll_list: Optional[List[V1MeetingsMeetingIdEnrollImportPost200ResponseEnrollListInner] | List[Dict[str, Any]]] = None,
        total_count: Optional[int] = None,
        user_non_registered: Optional[List[str]] = None,
        **kwargs
    ):
        
        if enroll_list and isinstance(enroll_list, (list, List)):
            self.enroll_list = [V1MeetingsMeetingIdEnrollImportPost200ResponseEnrollListInner(**_item) if isinstance(_item, (dict, Dict)) else _item for _item in enroll_list]
        
        self.total_count = total_count
        
        if user_non_registered and isinstance(user_non_registered, (list, List)):
            self.user_non_registered = user_non_registered
        

