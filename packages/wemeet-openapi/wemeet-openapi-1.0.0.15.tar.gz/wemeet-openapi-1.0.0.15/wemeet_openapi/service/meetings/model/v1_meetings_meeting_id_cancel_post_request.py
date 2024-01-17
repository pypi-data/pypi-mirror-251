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


class V1MeetingsMeetingIdCancelPostRequest(object):
    """V1MeetingsMeetingIdCancelPostRequest

    :param instanceid: 用户的终端设备类型： 0：PSTN 1：PC 2：Mac 3：Android 4：iOS 5：Web 6：iPad 7：Android Pad 8：小程序 9：voip、sip 设备 10：linux 20：Rooms for Touch Windows 21：Rooms for Touch MacOS 22：Rooms for Touch Android 30：Controller for Touch Windows 32：Controller for Touch Android 33：Controller for Touch iOS (required) 
    :type instanceid: int

    :param meeting_type: 会议类型，默认值为0。 0：普通会议 1：周期性会议 
    :type meeting_type: Optional[int]

    :param reason_code: 原因代码，可为用户自定义 (required) 
    :type reason_code: int

    :param reason_detail: 取消原因描述 
    :type reason_detail: Optional[str]

    :param sub_meeting_id: 周期性子会议 ID，如果不传，则会取消该系列的周期性会议 
    :type sub_meeting_id: Optional[str]

    :param userid: 调用 API 的用户 ID（企业内部请使用企业唯一用户标识；OAuth2.0 鉴权用户请使用 openId）。 企业唯一用户标识说明： 1：企业对接 SSO 时使用的员工唯一标识 ID。 2：企业调用创建用户接口时传递的 userid 参数。  (required) 
    :type userid: str
    """  # noqa: E501

    instanceid: int
    meeting_type: Optional[int] = None
    reason_code: int
    reason_detail: Optional[str] = None
    sub_meeting_id: Optional[str] = None
    userid: str
    additional_properties: Dict[str, Any] = {}

    def __init__(
        self,
        instanceid: int,
        reason_code: int,
        userid: str,
        meeting_type: Optional[int] = None,
        reason_detail: Optional[str] = None,
        sub_meeting_id: Optional[str] = None,
        **kwargs
    ):
        self.instanceid = instanceid
        self.meeting_type = meeting_type
        self.reason_code = reason_code
        self.reason_detail = reason_detail
        self.sub_meeting_id = sub_meeting_id
        self.userid = userid

