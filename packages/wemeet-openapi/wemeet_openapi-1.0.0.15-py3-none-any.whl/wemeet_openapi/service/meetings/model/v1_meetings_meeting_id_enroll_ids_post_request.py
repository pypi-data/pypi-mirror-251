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


class V1MeetingsMeetingIdEnrollIdsPostRequest(object):
    """V1MeetingsMeetingIdEnrollIdsPostRequest

    :param instanceid: 用户的终端设备类型： 0：PSTN 1：PC 2：Mac 3：Android 4：iOS 5：Web 6：iPad 7：Android Pad 8：小程序 9：voip、sip 设备 10：linux 20：Rooms for Touch Windows 21：Rooms for Touch MacOS 22：Rooms for Touch Android 30：Controller for Touch Windows 32：Controller for Touch Android 33：Controller for Touch iOS (required) 
    :type instanceid: int

    :param ms_open_id_list: 当场会议的用户临时 ID（适用于所有用户）数组，单次最多支持500条。 (required) 
    :type ms_open_id_list: List[str]

    :param operator_id: 操作者 ID。会议创建者可以导入报名信息。 operator_id 必须与 operator_id_type 配合使用。根据 operator_id_type 的值，operator_id 代表不同类型。 operator_id_type=2，operator_id 必须和公共参数的 openid 一致。 operator_id 和 userid 至少填写一个，两个参数如果都传了以 operator_id 为准。 使用 OAuth 公参鉴权后不能使用 userid 为入参。 
    :type operator_id: Optional[str]

    :param operator_id_type: 操作者 ID 的类型： 1：userid 2：open_id 如果 operator_id 和 userid 具有值，则以 operator_id 为准。 
    :type operator_id_type: Optional[int]

    :param sorting_rules: 查询报名 ID 的排序规则。当该账号存在多条报名记录（手机号导入、手动报名等）时，该接口返回的顺序。 1：优先查询手机号导入报名，再查询用户手动报名，默认值。 2：优先查询用户手动报名，再查手机号导入。 
    :type sorting_rules: Optional[int]

    :param userid: 会议创建者的用户 ID。为了防止现网应用报错，此参数实则仍然兼容 openid，如无 oauth 应用使用报名接口则也可做成不兼容变更。 
    :type userid: Optional[str]
    """  # noqa: E501

    instanceid: int
    ms_open_id_list: List[str]
    operator_id: Optional[str] = None
    operator_id_type: Optional[int] = None
    sorting_rules: Optional[int] = None
    userid: Optional[str] = None
    additional_properties: Dict[str, Any] = {}

    def __init__(
        self,
        instanceid: int,
        ms_open_id_list: List[str],
        operator_id: Optional[str] = None,
        operator_id_type: Optional[int] = None,
        sorting_rules: Optional[int] = None,
        userid: Optional[str] = None,
        **kwargs
    ):
        self.instanceid = instanceid
        
        if ms_open_id_list and isinstance(ms_open_id_list, (list, List)):
            self.ms_open_id_list = ms_open_id_list
        
        self.operator_id = operator_id
        self.operator_id_type = operator_id_type
        self.sorting_rules = sorting_rules
        self.userid = userid

