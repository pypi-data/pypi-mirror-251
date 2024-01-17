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


class V1MeetingsMeetingIdEnrollImportPostRequestEnrollListInner(object):
    """V1MeetingsMeetingIdEnrollImportPostRequestEnrollListInner

    :param area: 国家/地区代码，若使用手机号，必填（例如：中国传86，不是+86） 
    :type area: Optional[str]

    :param nick_name: 报名的昵称，与会中昵称可能不一致 
    :type nick_name: Optional[str]

    :param open_id: OAuth授权用户ID。  导入报名对象支持本企业（或与OAuth应用同企业）内 userid、授权用户的openid、phone_number 三种形式，三者必填其一；  如果都传了以openid为准；（优先级为：openid -> userid -> phone_number）  JWT鉴权方式无法使用open_id导入报名。 
    :type open_id: Optional[str]

    :param phone_number: 手机号,导入报名支持本企业（或与OAuth应用同企业）内 userid、授权用户的openid、phone_number 三种形式，三者必填其一。 
    :type phone_number: Optional[str]

    :param userid: 用户的唯一 ID（企业内部请使用企业唯一用户标识）。 导入报名支持本企业（或与OAuth应用同企业）内 userid、授权用户的openid、phone_number 三种形式，三者必填其一。 
    :type userid: Optional[str]
    """  # noqa: E501

    area: Optional[str] = None
    nick_name: Optional[str] = None
    open_id: Optional[str] = None
    phone_number: Optional[str] = None
    userid: Optional[str] = None
    additional_properties: Dict[str, Any] = {}

    def __init__(
        self,
        area: Optional[str] = None,
        nick_name: Optional[str] = None,
        open_id: Optional[str] = None,
        phone_number: Optional[str] = None,
        userid: Optional[str] = None,
        **kwargs
    ):
        self.area = area
        self.nick_name = nick_name
        self.open_id = open_id
        self.phone_number = phone_number
        self.userid = userid

