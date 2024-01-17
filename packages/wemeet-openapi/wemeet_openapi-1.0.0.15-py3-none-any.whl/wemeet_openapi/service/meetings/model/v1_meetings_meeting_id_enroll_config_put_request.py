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
from wemeet_openapi.service.meetings.model.v1_meetings_meeting_id_enroll_config_put_request_question_list_inner import V1MeetingsMeetingIdEnrollConfigPutRequestQuestionListInner


class V1MeetingsMeetingIdEnrollConfigPutRequest(object):
    """V1MeetingsMeetingIdEnrollConfigPutRequest

    :param approve_type: 审批类型：1 自动审批，2 手动审批，默认自动审批 
    :type approve_type: Optional[int]

    :param cover_image: 报名封面图的URL，上传封面为异步形式，通过异步任务结果webhook获取上传结果，列表内容为空字符串时为默认图片，不传或传空列表则不做修改，最多支持5张，支持格式为jpg，jpeg，png。每张不超过5M，按照传入顺序展示。 
    :type cover_image: Optional[List[str]]

    :param display_number_of_participants: 显示已报名/预约人数。0：不展示 1：展示，默认开启 
    :type display_number_of_participants: Optional[int]

    :param enroll_deadline: 报名截止时间（秒级时间戳） 
    :type enroll_deadline: Optional[str]

    :param enroll_description: 报名页详情介绍，最多5000字符 
    :type enroll_description: Optional[str]

    :param enroll_number: 报名人数上限 
    :type enroll_number: Optional[int]

    :param enroll_push_type: 报名审批自动通知方式，1-短信通知；2-邮件中文；3-邮件英文；4-邮件中英文；5-公众号 
    :type enroll_push_type: Optional[List[int]]

    :param instanceid: 设备类型 (required) 
    :type instanceid: int

    :param is_collect_question: 是否收集问题：1 不收集，2 收集，默认不收集问题 
    :type is_collect_question: Optional[int]

    :param no_registration_needed_for_staff: 本企业用户无需报名。 true: 本企业用户无需报名。 false：默认配置，所有用户需要报名。  
    :type no_registration_needed_for_staff: Optional[bool]

    :param operator_id: 操作者 ID。会议创建者可以导入报名信息。 operator_id 必须与 operator_id_type 配合使用。根据 operator_id_type 的值，operator_id 代表不同类型。  operator_id_type=2，operator_id必须和公共参数的openid一致。  operator_id和userid至少填写一个，两个参数如果都传了以operator_id为准。  使用OAuth公参鉴权后不能使用userid为入参。 
    :type operator_id: Optional[str]

    :param operator_id_type: 操作者 ID 的类型：  1: userid 2: open_id  如果operator_id和userid具有值，则以operator_id为准； 
    :type operator_id_type: Optional[int]

    :param question_list: 报名问题列表，非特殊问题按传入的顺序排序，特殊问题会优先放在最前面，仅开启收集问题时有效 
    :type question_list: Optional[List[V1MeetingsMeetingIdEnrollConfigPutRequestQuestionListInner]]

    :param userid: 用户id 
    :type userid: Optional[str]
    """  # noqa: E501

    approve_type: Optional[int] = None
    cover_image: Optional[List[str]] = None
    display_number_of_participants: Optional[int] = None
    enroll_deadline: Optional[str] = None
    enroll_description: Optional[str] = None
    enroll_number: Optional[int] = None
    enroll_push_type: Optional[List[int]] = None
    instanceid: int
    is_collect_question: Optional[int] = None
    no_registration_needed_for_staff: Optional[bool] = None
    operator_id: Optional[str] = None
    operator_id_type: Optional[int] = None
    question_list: Optional[List[V1MeetingsMeetingIdEnrollConfigPutRequestQuestionListInner]] = None
    userid: Optional[str] = None
    additional_properties: Dict[str, Any] = {}

    def __init__(
        self,
        instanceid: int,
        approve_type: Optional[int] = None,
        cover_image: Optional[List[str]] = None,
        display_number_of_participants: Optional[int] = None,
        enroll_deadline: Optional[str] = None,
        enroll_description: Optional[str] = None,
        enroll_number: Optional[int] = None,
        enroll_push_type: Optional[List[int]] = None,
        is_collect_question: Optional[int] = None,
        no_registration_needed_for_staff: Optional[bool] = None,
        operator_id: Optional[str] = None,
        operator_id_type: Optional[int] = None,
        question_list: Optional[List[V1MeetingsMeetingIdEnrollConfigPutRequestQuestionListInner] | List[Dict[str, Any]]] = None,
        userid: Optional[str] = None,
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
        
        self.instanceid = instanceid
        self.is_collect_question = is_collect_question
        self.no_registration_needed_for_staff = no_registration_needed_for_staff
        self.operator_id = operator_id
        self.operator_id_type = operator_id_type
        
        if question_list and isinstance(question_list, (list, List)):
            self.question_list = [V1MeetingsMeetingIdEnrollConfigPutRequestQuestionListInner(**_item) if isinstance(_item, (dict, Dict)) else _item for _item in question_list]
        
        self.userid = userid

