# coding: utf-8

"""
    腾讯会议OpenAPI

    SAAS版RESTFUL风格API

    API version: v1.0.0.16

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations

from typing import *

# import models into model package
from wemeet_openapi.service.meetings.model.v1_meetings_meeting_id_enroll_config_get200_response_question_list_inner_option_list_inner import V1MeetingsMeetingIdEnrollConfigGet200ResponseQuestionListInnerOptionListInner


class V1MeetingsMeetingIdEnrollConfigGet200ResponseQuestionListInner(object):
    """V1MeetingsMeetingIdEnrollConfigGet200ResponseQuestionListInner

    :param is_required: 是否必填：1 否，2 是 
    :type is_required: Optional[int]

    :param option_list: 问题选项列表，按传入的顺序排序，仅单选/多选时有效，最多8个选项，每个选项限40个汉字 
    :type option_list: Optional[List[V1MeetingsMeetingIdEnrollConfigGet200ResponseQuestionListInnerOptionListInner]]

    :param question_title: 问题标题，限制40个汉字 
    :type question_title: Optional[str]

    :param question_type: 问题类型：1 单选，2 多选，3 简答 
    :type question_type: Optional[int]

    :param special_type: 特殊问题类型：1 无，2 手机号，3 邮箱，4 姓名，5 组织名称，6 组织规模（目前除组织规模外均为简答题，组织规模为单选题） 
    :type special_type: Optional[int]
    """  # noqa: E501

    is_required: Optional[int] = None
    option_list: Optional[List[V1MeetingsMeetingIdEnrollConfigGet200ResponseQuestionListInnerOptionListInner]] = None
    question_title: Optional[str] = None
    question_type: Optional[int] = None
    special_type: Optional[int] = None
    additional_properties: Dict[str, Any] = {}

    def __init__(
        self,
        is_required: Optional[int] = None,
        option_list: Optional[List[V1MeetingsMeetingIdEnrollConfigGet200ResponseQuestionListInnerOptionListInner] | List[Dict[str, Any]]] = None,
        question_title: Optional[str] = None,
        question_type: Optional[int] = None,
        special_type: Optional[int] = None,
        **kwargs
    ):
        self.is_required = is_required
        
        if option_list and isinstance(option_list, (list, List)):
            self.option_list = [V1MeetingsMeetingIdEnrollConfigGet200ResponseQuestionListInnerOptionListInner(**_item) if isinstance(_item, (dict, Dict)) else _item for _item in option_list]
        
        self.question_title = question_title
        self.question_type = question_type
        self.special_type = special_type

