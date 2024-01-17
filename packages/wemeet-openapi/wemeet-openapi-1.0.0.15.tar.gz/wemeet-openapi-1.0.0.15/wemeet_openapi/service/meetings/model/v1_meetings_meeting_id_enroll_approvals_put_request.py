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


class V1MeetingsMeetingIdEnrollApprovalsPutRequest(object):
    """V1MeetingsMeetingIdEnrollApprovalsPutRequest

    :param action: 审批动作：1 取消批准，2 拒绝，3.批准，取消批准后状态将变成待审批 (required) 
    :type action: int

    :param enroll_id_list: 报名id列表效 (required) 
    :type enroll_id_list: List[int]

    :param instanceid: 设备类型 
    :type instanceid: Optional[int]

    :param operator_id: 操作者 ID。会议创建者可以导入报名信息。 operator_id 必须与 operator_id_type 配合使用。根据 operator_id_type 的值，operator_id 代表不同类型。  operator_id_type=2，operator_id必须和公共参数的openid一致。  operator_id和userid至少填写一个，两个参数如果都传了以operator_id为准。  使用OAuth公参鉴权后不能使用userid为入参。 
    :type operator_id: Optional[str]

    :param operator_id_type: 操作者 ID 的类型：  1: userid 2: open_id  如果operator_id和userid具有值，则以operator_id为准； (required) 
    :type operator_id_type: int

    :param userid: 用户id 
    :type userid: Optional[str]
    """  # noqa: E501

    action: int
    enroll_id_list: List[int]
    instanceid: Optional[int] = None
    operator_id: Optional[str] = None
    operator_id_type: int
    userid: Optional[str] = None
    additional_properties: Dict[str, Any] = {}

    def __init__(
        self,
        action: int,
        enroll_id_list: List[int],
        operator_id_type: int,
        instanceid: Optional[int] = None,
        operator_id: Optional[str] = None,
        userid: Optional[str] = None,
        **kwargs
    ):
        self.action = action
        
        if enroll_id_list and isinstance(enroll_id_list, (list, List)):
            self.enroll_id_list = enroll_id_list
        
        self.instanceid = instanceid
        self.operator_id = operator_id
        self.operator_id_type = operator_id_type
        self.userid = userid

