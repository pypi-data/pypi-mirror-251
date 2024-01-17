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


class V1MeetingsMeetingIdEnrollApprovalsGet200ResponseEnrollListInnerAnswerListInner(object):
    """V1MeetingsMeetingIdEnrollApprovalsGet200ResponseEnrollListInnerAnswerListInner

    :param answer_content: 回答内容：单选/简答只有一个元素，多选会有多个 
    :type answer_content: Optional[List[str]]

    :param is_required: 是否必填：1 否，2 是 
    :type is_required: Optional[int]

    :param question_num: 问题编号，1,2,3...等形式 
    :type question_num: Optional[int]

    :param question_title: 问题标题 
    :type question_title: Optional[str]

    :param question_type: 问题类型：1 单选，2 多选，3 简答 
    :type question_type: Optional[int]

    :param special_type: 特殊问题类型：1 无，2 手机号，3 邮箱，4 姓名，5 公司名称（目前4种特殊问题均为简答题） 
    :type special_type: Optional[int]
    """  # noqa: E501

    answer_content: Optional[List[str]] = None
    is_required: Optional[int] = None
    question_num: Optional[int] = None
    question_title: Optional[str] = None
    question_type: Optional[int] = None
    special_type: Optional[int] = None
    additional_properties: Dict[str, Any] = {}

    def __init__(
        self,
        answer_content: Optional[List[str]] = None,
        is_required: Optional[int] = None,
        question_num: Optional[int] = None,
        question_title: Optional[str] = None,
        question_type: Optional[int] = None,
        special_type: Optional[int] = None,
        **kwargs
    ):
        
        if answer_content and isinstance(answer_content, (list, List)):
            self.answer_content = answer_content
        
        self.is_required = is_required
        self.question_num = question_num
        self.question_title = question_title
        self.question_type = question_type
        self.special_type = special_type

