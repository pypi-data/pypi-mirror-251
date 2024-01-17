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


class V1MeetingSetWaitingRoomWelcomeMessagePost200Response(object):
    """V1MeetingSetWaitingRoomWelcomeMessagePost200Response

    :param enable_welcome: 是否开启等候室欢迎语能力。 
    :type enable_welcome: Optional[bool]

    :param welcome_text: 欢迎语，文本类型，最大长度1000字符。欢迎语中如果传入占位符%NICKNAME%（大小写敏感），则该占位符会被替换为被私聊用户的会中昵称。一条消息中支持多个占位符。 
    :type welcome_text: Optional[str]
    """  # noqa: E501

    enable_welcome: Optional[bool] = None
    welcome_text: Optional[str] = None
    additional_properties: Dict[str, Any] = {}

    def __init__(
        self,
        enable_welcome: Optional[bool] = None,
        welcome_text: Optional[str] = None,
        **kwargs
    ):
        self.enable_welcome = enable_welcome
        self.welcome_text = welcome_text

