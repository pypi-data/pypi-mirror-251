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
from wemeet_openapi.service.meetings.model.v1_meetings_meeting_id_enroll_import_post_request_enroll_list_inner import V1MeetingsMeetingIdEnrollImportPostRequestEnrollListInner


class V1MeetingsMeetingIdEnrollImportPostRequest(object):
    """V1MeetingsMeetingIdEnrollImportPostRequest

    :param enroll_list: 导入的报名对象列表，单次导入最大1000条。累计导入最大4000 (required) 
    :type enroll_list: List[V1MeetingsMeetingIdEnrollImportPostRequestEnrollListInner]

    :param instanceid: 操作者的终端设备类型 (required) 
    :type instanceid: int

    :param operator_id: 操作者 ID。operator_id 必须与 operator_id_type 配合使用。根据 operator_id_type 的值，operator_id 代表不同类型。operator_id_type=2，operator_id必须和公共参数的openid一致。  使用OAuth公参鉴权后不能使用userid为入参。 (required) 
    :type operator_id: str

    :param operator_id_type: 操作者 ID 的类型： 1. 企业用户 userid 2 open_id (required) 
    :type operator_id_type: int
    """  # noqa: E501

    enroll_list: List[V1MeetingsMeetingIdEnrollImportPostRequestEnrollListInner]
    instanceid: int
    operator_id: str
    operator_id_type: int
    additional_properties: Dict[str, Any] = {}

    def __init__(
        self,
        enroll_list: List[V1MeetingsMeetingIdEnrollImportPostRequestEnrollListInner] | List[Dict[str, Any]],
        instanceid: int,
        operator_id: str,
        operator_id_type: int,
        **kwargs
    ):
        
        if enroll_list and isinstance(enroll_list, (list, List)):
            self.enroll_list = [V1MeetingsMeetingIdEnrollImportPostRequestEnrollListInner(**_item) if isinstance(_item, (dict, Dict)) else _item for _item in enroll_list]
        
        self.instanceid = instanceid
        self.operator_id = operator_id
        self.operator_id_type = operator_id_type

