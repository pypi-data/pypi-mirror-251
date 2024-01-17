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
from wemeet_openapi.service.meetings.model.v1_meetings_meeting_id_enroll_approvals_get200_response_enroll_list_inner import V1MeetingsMeetingIdEnrollApprovalsGet200ResponseEnrollListInner


class V1MeetingsMeetingIdEnrollApprovalsGet200Response(object):
    """V1MeetingsMeetingIdEnrollApprovalsGet200Response

    :param current_page: 当前页 
    :type current_page: Optional[int]

    :param current_size: 当前页实际大小 
    :type current_size: Optional[int]

    :param enroll_list: 当前页的报名列表，current_size为0时无该字段 
    :type enroll_list: Optional[List[V1MeetingsMeetingIdEnrollApprovalsGet200ResponseEnrollListInner]]

    :param total_count: 根据条件筛选后的总报名人数 
    :type total_count: Optional[int]

    :param total_page: 根据条件筛选后的总分页数 
    :type total_page: Optional[int]
    """  # noqa: E501

    current_page: Optional[int] = None
    current_size: Optional[int] = None
    enroll_list: Optional[List[V1MeetingsMeetingIdEnrollApprovalsGet200ResponseEnrollListInner]] = None
    total_count: Optional[int] = None
    total_page: Optional[int] = None
    additional_properties: Dict[str, Any] = {}

    def __init__(
        self,
        current_page: Optional[int] = None,
        current_size: Optional[int] = None,
        enroll_list: Optional[List[V1MeetingsMeetingIdEnrollApprovalsGet200ResponseEnrollListInner] | List[Dict[str, Any]]] = None,
        total_count: Optional[int] = None,
        total_page: Optional[int] = None,
        **kwargs
    ):
        self.current_page = current_page
        self.current_size = current_size
        
        if enroll_list and isinstance(enroll_list, (list, List)):
            self.enroll_list = [V1MeetingsMeetingIdEnrollApprovalsGet200ResponseEnrollListInner(**_item) if isinstance(_item, (dict, Dict)) else _item for _item in enroll_list]
        
        self.total_count = total_count
        self.total_page = total_page

