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
from wemeet_openapi.service.meetings.model.v1_meetings_meeting_id_enroll_config_get200_response_question_list_inner import V1MeetingsMeetingIdEnrollConfigGet200ResponseQuestionListInner


class V1MeetingsMeetingIdEnrollConfigGet200Response(object):
    """V1MeetingsMeetingIdEnrollConfigGet200Response

    :param approve_type: 审批类型：1 自动审批，2 手动审批，默认自动审批 
    :type approve_type: Optional[int]

    :param cover_image: 报名页封面图URL（base64编码） 
    :type cover_image: Optional[List[str]]

    :param display_number_of_participants: 显示已报名/预约人数。0：不展示 1：展示，默认开启 
    :type display_number_of_participants: Optional[int]

    :param enroll_deadline: 报名截止时间（秒级时间戳） 
    :type enroll_deadline: Optional[str]

    :param enroll_description: 报名页简介 
    :type enroll_description: Optional[str]

    :param enroll_number: 报名人数上限 
    :type enroll_number: Optional[int]

    :param enroll_push_type: 报名审批自动通知方式，1-短信通知；2-邮件中文；3-邮件英文；4-邮件中英文；5-公众号 
    :type enroll_push_type: Optional[List[int]]

    :param is_collect_question: 是否收集问题：1 不收集，2 收集，默认不收集问题 
    :type is_collect_question: Optional[int]

    :param meeting_id: 会议id 
    :type meeting_id: Optional[str]

    :param no_registration_needed_for_staff: 本企业用户无需报名。 true: 本企业用户无需报名。 false：默认配置，所有用户需要报名。  
    :type no_registration_needed_for_staff: Optional[bool]

    :param question_list: 报名问题列表，自定义问题按传入的顺序排序，预设问题会优先放在最前面，仅开启收集问题时有效 
    :type question_list: Optional[List[V1MeetingsMeetingIdEnrollConfigGet200ResponseQuestionListInner]]
    """  # noqa: E501

    approve_type: Optional[int] = None
    cover_image: Optional[List[str]] = None
    display_number_of_participants: Optional[int] = None
    enroll_deadline: Optional[str] = None
    enroll_description: Optional[str] = None
    enroll_number: Optional[int] = None
    enroll_push_type: Optional[List[int]] = None
    is_collect_question: Optional[int] = None
    meeting_id: Optional[str] = None
    no_registration_needed_for_staff: Optional[bool] = None
    question_list: Optional[List[V1MeetingsMeetingIdEnrollConfigGet200ResponseQuestionListInner]] = None
    additional_properties: Dict[str, Any] = {}

    def __init__(
        self,
        approve_type: Optional[int] = None,
        cover_image: Optional[List[str]] = None,
        display_number_of_participants: Optional[int] = None,
        enroll_deadline: Optional[str] = None,
        enroll_description: Optional[str] = None,
        enroll_number: Optional[int] = None,
        enroll_push_type: Optional[List[int]] = None,
        is_collect_question: Optional[int] = None,
        meeting_id: Optional[str] = None,
        no_registration_needed_for_staff: Optional[bool] = None,
        question_list: Optional[List[V1MeetingsMeetingIdEnrollConfigGet200ResponseQuestionListInner] | List[Dict[str, Any]]] = None,
        **kwargs
    ):
        self.approve_type = approve_type
        
        if cover_image and isinstance(cover_image, (list, List)):
            self.cover_image = cover_image
        
        self.display_number_of_participants = display_number_of_participants
        self.enroll_deadline = enroll_deadline
        self.enroll_description = enroll_description
        self.enroll_number = enroll_number
        
        if enroll_push_type and isinstance(enroll_push_type, (list, List)):
            self.enroll_push_type = enroll_push_type
        
        self.is_collect_question = is_collect_question
        self.meeting_id = meeting_id
        self.no_registration_needed_for_staff = no_registration_needed_for_staff
        
        if question_list and isinstance(question_list, (list, List)):
            self.question_list = [V1MeetingsMeetingIdEnrollConfigGet200ResponseQuestionListInner(**_item) if isinstance(_item, (dict, Dict)) else _item for _item in question_list]
        

