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
from wemeet_openapi.service.meetings.model.v1_meetings_meeting_id_enroll_approvals_get200_response_enroll_list_inner_answer_list_inner import V1MeetingsMeetingIdEnrollApprovalsGet200ResponseEnrollListInnerAnswerListInner


class V1MeetingsMeetingIdEnrollApprovalsGet200ResponseEnrollListInner(object):
    """V1MeetingsMeetingIdEnrollApprovalsGet200ResponseEnrollListInner

    :param answer_list: 答题列表 
    :type answer_list: Optional[List[V1MeetingsMeetingIdEnrollApprovalsGet200ResponseEnrollListInnerAnswerListInner]]

    :param enroll_code: pstn入会凭证 
    :type enroll_code: Optional[str]

    :param enroll_id: 报名id 
    :type enroll_id: Optional[int]

    :param enroll_source_type: 报名来源： 1：用户手动报名 2：批量导入报名 
    :type enroll_source_type: Optional[int]

    :param enroll_time: 报名时间（utc+8，非时间戳） 
    :type enroll_time: Optional[str]

    :param ms_open_id: 当场会议的用户临时id，所有用户都有 
    :type ms_open_id: Optional[str]

    :param nick_name: 昵称 
    :type nick_name: Optional[str]

    :param open_id: 报名者已授权过会议创建的应用时返回openid，否则为空 
    :type open_id: Optional[str]

    :param status: 报名状态：1 待审批，2 已拒绝，3 已批准 
    :type status: Optional[int]

    :param userid: 报名者与会议创建者为同企业时，返回userid，否则为空,导入报名入参为手机号的情况不返回userid。 
    :type userid: Optional[str]
    """  # noqa: E501

    answer_list: Optional[List[V1MeetingsMeetingIdEnrollApprovalsGet200ResponseEnrollListInnerAnswerListInner]] = None
    enroll_code: Optional[str] = None
    enroll_id: Optional[int] = None
    enroll_source_type: Optional[int] = None
    enroll_time: Optional[str] = None
    ms_open_id: Optional[str] = None
    nick_name: Optional[str] = None
    open_id: Optional[str] = None
    status: Optional[int] = None
    userid: Optional[str] = None
    additional_properties: Dict[str, Any] = {}

    def __init__(
        self,
        answer_list: Optional[List[V1MeetingsMeetingIdEnrollApprovalsGet200ResponseEnrollListInnerAnswerListInner] | List[Dict[str, Any]]] = None,
        enroll_code: Optional[str] = None,
        enroll_id: Optional[int] = None,
        enroll_source_type: Optional[int] = None,
        enroll_time: Optional[str] = None,
        ms_open_id: Optional[str] = None,
        nick_name: Optional[str] = None,
        open_id: Optional[str] = None,
        status: Optional[int] = None,
        userid: Optional[str] = None,
        **kwargs
    ):
        
        if answer_list and isinstance(answer_list, (list, List)):
            self.answer_list = [V1MeetingsMeetingIdEnrollApprovalsGet200ResponseEnrollListInnerAnswerListInner(**_item) if isinstance(_item, (dict, Dict)) else _item for _item in answer_list]
        
        self.enroll_code = enroll_code
        self.enroll_id = enroll_id
        self.enroll_source_type = enroll_source_type
        self.enroll_time = enroll_time
        self.ms_open_id = ms_open_id
        self.nick_name = nick_name
        self.open_id = open_id
        self.status = status
        self.userid = userid

