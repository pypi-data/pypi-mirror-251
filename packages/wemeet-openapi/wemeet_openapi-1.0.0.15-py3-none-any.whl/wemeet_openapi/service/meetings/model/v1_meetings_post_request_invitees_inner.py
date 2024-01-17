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


class V1MeetingsPostRequestInviteesInner(object):
    """V1MeetingsPostRequestInviteesInner

    :param is_anonymous: 用户是否匿名入会，缺省为 false，不匿名。 true：匿名 false：不匿名 
    :type is_anonymous: Optional[bool]

    :param nick_name: 用户匿名字符串。如果字段“is_anonymous”设置为“true”，但是无指定匿名字符串, 会议将分配缺省名称，例如 “会议用户xxxx”，其中“xxxx”为随机数字。 
    :type nick_name: Optional[str]

    :param userid: 用户 ID（企业内部请使用企业唯一用户标识；OAuth2.0 鉴权用户请使用 openId）。 企业唯一用户标识说明： 企业对接 SSO 时使用的员工唯一标识 ID，企业调用创建用户接口时传递的 userid 参数。 (required) 
    :type userid: str
    """  # noqa: E501

    is_anonymous: Optional[bool] = None
    nick_name: Optional[str] = None
    userid: str
    additional_properties: Dict[str, Any] = {}

    def __init__(
        self,
        userid: str,
        is_anonymous: Optional[bool] = None,
        nick_name: Optional[str] = None,
        **kwargs
    ):
        self.is_anonymous = is_anonymous
        self.nick_name = nick_name
        self.userid = userid

