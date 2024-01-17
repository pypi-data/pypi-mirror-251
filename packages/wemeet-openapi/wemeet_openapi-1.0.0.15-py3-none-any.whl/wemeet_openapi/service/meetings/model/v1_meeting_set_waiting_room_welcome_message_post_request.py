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


class V1MeetingSetWaitingRoomWelcomeMessagePostRequest(object):
    """V1MeetingSetWaitingRoomWelcomeMessagePostRequest

    :param enable_welcome: 是否开启等候室欢迎语能力。 (required) 
    :type enable_welcome: bool

    :param meeting_id: 会议ID (required) 
    :type meeting_id: str

    :param operator_id: 操作者 ID，设置等候室欢迎语的用户。会议的创建者、主持人、联席主持人，企业管理平台有会控权限的用户可以设置。  operator_id 必须与 operator_id_type 配合使用。根据 operator_id_type 的值，operator_id 代表不同类型。 (required) 
    :type operator_id: str

    :param operator_id_type: 操作者 ID 的类型： 1: 企业内用户 userid。 2: open_id (required) 
    :type operator_id_type: float

    :param welcome_text: 欢迎语，文本类型，最大长度1000字符。欢迎语中如果传入占位符%NICKNAME%（大小写敏感），则该占位符会被替换为被私聊用户的会中昵称。一条消息中支持多个占位符。 (required) 
    :type welcome_text: str
    """  # noqa: E501

    enable_welcome: bool
    meeting_id: str
    operator_id: str
    operator_id_type: float
    welcome_text: str
    additional_properties: Dict[str, Any] = {}

    def __init__(
        self,
        enable_welcome: bool,
        meeting_id: str,
        operator_id: str,
        operator_id_type: float,
        welcome_text: str,
        **kwargs
    ):
        self.enable_welcome = enable_welcome
        self.meeting_id = meeting_id
        self.operator_id = operator_id
        self.operator_id_type = operator_id_type
        self.welcome_text = welcome_text

