# coding: utf-8

"""
    腾讯会议OpenAPI

    SAAS版RESTFUL风格API

    API version: v1.0.0.15

    Do not edit the class manually.
"""  # noqa: E501


from typing import Dict, List, Optional, Callable

from wemeet_openapi.core import Config, DEFAULT_AUTHENTICATOR, DEFAULT_SERIALIZER
from wemeet_openapi.core.xhttp import ApiRequest, ApiResponse
from wemeet_openapi.core.authenticator import Authenticator
from wemeet_openapi.core.serializer import Serializer
from wemeet_openapi.core.exception import ServiceException, ClientException
from wemeet_openapi.service.meetings.model import *


class ApiV1MeetingSetWaitingRoomWelcomeMessagePostRequest(object):
    """设置等候室欢迎语

    为已开启等候室的会议配置等候室欢迎语。当有用户进入等候室时，会收到来自会议主办方的私聊消息引导。  鉴权方式: JWT鉴权、OAuth鉴权
    
    :param body:
    :type body: V1MeetingSetWaitingRoomWelcomeMessagePostRequest
    """  # noqa: E501

    def __init__(
        self,
        body: Optional[V1MeetingSetWaitingRoomWelcomeMessagePostRequest] = None
    ):
        self.body = body


class ApiV1MeetingSetWaitingRoomWelcomeMessagePostResponse(ApiResponse):
    data: Optional[V1MeetingSetWaitingRoomWelcomeMessagePost200Response] = None

    def __init__(self, api_resp: ApiResponse, data: Optional[V1MeetingSetWaitingRoomWelcomeMessagePost200Response] = None):
        super().__init__(
            status_code=api_resp.status_code,
            raw_body=api_resp.raw_body,
            header=api_resp.header,
            serializer=api_resp.serializer()
        )
        self.data = data


class ApiV1MeetingsGetRequest(object):
    """通过会议CODE查询会议列表

    通过会议 ID 查询会议详情。 企业 secret 鉴权用户可查询到任何该用户创建的企业下的会议，OAuth2.0 鉴权用户只能查询到通过 OAuth2.0 鉴权创建的会议。 支持企业管理员查询企业下的会议。 本接口的邀请参会成员限制调整至300人。 当会议为周期性会议时，主持人密钥每场会议固定，但单场会议只能获取一次。支持查询周期性会议的主持人密钥。 支持查询 MRA 当前所在会议信息。 若会议号被回收则无法通过 Code 查询，您可以通过会议 ID 查询到该会议。
    
    :param instanceid: 用户的终端设备类型： 0：PSTN 1：PC 2：Mac 3：Android 4：iOS 5：Web 6：iPad 7：Android Pad 8：小程序 9：voip、sip 设备 10：Linux 20：Rooms for Touch Windows 21：Rooms for Touch MacOS 22：Rooms for Touch Android 30：Controller for Touch Windows 32：Controller for Touch Android 33：Controller for Touch iOS (required)
    :type instanceid: str

    :param meeting_code: 有效的9位数字会议号码。 (required)
    :type meeting_code: str

    :param operator_id: 操作者 ID。operator_id 必须与 operator_id_type 配合使用。根据 operator_id_type 的值，operator_id 代表不同类型。 说明：userid 字段和 operator_id 字段二者必填一项。若两者都填，以 operator_id 字段为准。
    :type operator_id: str

    :param operator_id_type: 操作者 ID 的类型： 3：rooms_id 说明：当前仅支持 rooms_id。如操作者为企业内 userid 或 openId，请使用 userid 字段。
    :type operator_id_type: str

    :param userid: 调用方用于标示用户的唯一 ID（企业内部请使用企业唯一用户标识；OAuth2.0 鉴权用户请使用 openId）。 企业唯一用户标识说明： 1：企业对接 SSO 时使用的员工唯一标识 ID。 2：企业调用创建用户接口时传递的 userid 参数。
    :type userid: str

    :param cursory: 分页游标
    :type cursory: str

    :param pos: 分页获取用户会议列表的查询起始时间值，unix 秒级时间戳
    :type pos: str

    :param is_show_all_sub_meetings: 是否显示周期性会议的所有子会议，默认值为0。 0：只显示周期性会议的第一个子会议 1：显示所有周期性会议的子会议
    :type is_show_all_sub_meetings: str

    :param body:
    :type body: object
    """  # noqa: E501

    def __init__(
        self,
        instanceid: Optional[str] = None,
        meeting_code: Optional[str] = None,
        operator_id: Optional[str] = None,
        operator_id_type: Optional[str] = None,
        userid: Optional[str] = None,
        cursory: Optional[str] = None,
        pos: Optional[str] = None,
        is_show_all_sub_meetings: Optional[str] = None,
        body: Optional[object] = None
    ):
        self.instanceid = instanceid
        self.meeting_code = meeting_code
        self.operator_id = operator_id
        self.operator_id_type = operator_id_type
        self.userid = userid
        self.cursory = cursory
        self.pos = pos
        self.is_show_all_sub_meetings = is_show_all_sub_meetings
        self.body = body


class ApiV1MeetingsGetResponse(ApiResponse):
    data: Optional[V1MeetingsGet200Response] = None

    def __init__(self, api_resp: ApiResponse, data: Optional[V1MeetingsGet200Response] = None):
        super().__init__(
            status_code=api_resp.status_code,
            raw_body=api_resp.raw_body,
            header=api_resp.header,
            serializer=api_resp.serializer()
        )
        self.data = data


class ApiV1MeetingsMeetingIdCancelPostRequest(object):
    """取消会议

    取消用户创建的会议。用户只能取消自己创建的会议，且该会议是一个有效的会议。如果不是会议创建者或者无效会议号将会返回错误。 企业 secret 鉴权用户可取消任何该用户企业下创建的有效会议，OAuth2.0 鉴权用户只能取消通过 OAuth2.0 鉴权创建的有效会议。 当您想实时监测会议取消状况时，您可以通过订阅 [会议取消](https://cloud.tencent.com/document/product/1095/51616) 的事件，接收事件通知。
    
    :param meeting_id: (required)
    :type meeting_id: str

    :param body:
    :type body: V1MeetingsMeetingIdCancelPostRequest
    """  # noqa: E501

    def __init__(
        self,
        meeting_id: str,
        body: Optional[V1MeetingsMeetingIdCancelPostRequest] = None
    ):
        self.meeting_id = meeting_id
        self.body = body


class ApiV1MeetingsMeetingIdCancelPostResponse(ApiResponse):
    data: Optional[object] = None

    def __init__(self, api_resp: ApiResponse, data: Optional[object] = None):
        super().__init__(
            status_code=api_resp.status_code,
            raw_body=api_resp.raw_body,
            header=api_resp.header,
            serializer=api_resp.serializer()
        )
        self.data = data


class ApiV1MeetingsMeetingIdEnrollApprovalsGetRequest(object):
    """查询会议报名信息

    查询已报名观众数量和报名观众答题详情，仅会议创建者可查询。 企业 secret 鉴权用户可修改任何该企业该用户创建的有效会议，OAuth2.0 鉴权用户只能修改通过 OAuth2.0 鉴权创建的有效会议。 用户必须是注册用户，请求头部 X-TC-Registered 字段必须传入为1。
    
    :param meeting_id: 会议ID (required)
    :type meeting_id: str

    :param instanceid: 用户的终端设备类型： 1：PC 2：Mac 3：Android 4：iOS 5：Web 6：iPad 7：Android Pad 8：小程序 (required)
    :type instanceid: str

    :param page: 当前页，页码起始值为1 (required)
    :type page: str

    :param page_size: 分页大小，最大50条 (required)
    :type page_size: str

    :param userid: 会议创建者的用户 ID（企业内部请使用企业唯一用户标识；OAuth2.0 鉴权用户请使用 openId）为了防止现网应用报错，此参数实则仍然兼容openid，如无oauth应用使用报名接口则也可做成不兼容变更。
    :type userid: str

    :param status: 审批状态筛选字段，审批状态：0 全部，1 待审批，2 已拒绝，3 已批准，默认返回全部
    :type status: str

    :param operator_id: 操作者 ID。会议创建者可以导入报名信息。 operator_id 必须与 operator_id_type 配合使用。根据 operator_id_type 的值，operator_id 代表不同类型。  operator_id_type=2，operator_id必须和公共参数的openid一致。  operator_id和userid至少填写一个，两个参数如果都传了以operator_id为准。  使用OAuth公参鉴权后不能使用userid为入参。
    :type operator_id: str

    :param operator_id_type: 操作者 ID 的类型：  1: userid 2: open_id  如果operator_id和userid具有值，则以operator_id为准；
    :type operator_id_type: str

    :param body:
    :type body: object
    """  # noqa: E501

    def __init__(
        self,
        meeting_id: str,
        instanceid: Optional[str] = None,
        page: Optional[str] = None,
        page_size: Optional[str] = None,
        userid: Optional[str] = None,
        status: Optional[str] = None,
        operator_id: Optional[str] = None,
        operator_id_type: Optional[str] = None,
        body: Optional[object] = None
    ):
        self.meeting_id = meeting_id
        self.instanceid = instanceid
        self.page = page
        self.page_size = page_size
        self.userid = userid
        self.status = status
        self.operator_id = operator_id
        self.operator_id_type = operator_id_type
        self.body = body


class ApiV1MeetingsMeetingIdEnrollApprovalsGetResponse(ApiResponse):
    data: Optional[V1MeetingsMeetingIdEnrollApprovalsGet200Response] = None

    def __init__(self, api_resp: ApiResponse, data: Optional[V1MeetingsMeetingIdEnrollApprovalsGet200Response] = None):
        super().__init__(
            status_code=api_resp.status_code,
            raw_body=api_resp.raw_body,
            header=api_resp.header,
            serializer=api_resp.serializer()
        )
        self.data = data


class ApiV1MeetingsMeetingIdEnrollApprovalsPutRequest(object):
    """审批云会议报名信息

    批量云会议的报名信息，仅会议创建者可审批。 企业 secret 鉴权用户可审批任何该企业该用户创建的有效会议，OAuth2.0 鉴权用户只能审批通过 OAuth2.0 鉴权创建的有效会议。 用户必须是注册用户，请求头部 X-TC-Registered 字段必须传入为1。
    
    :param meeting_id: 会议ID (required)
    :type meeting_id: str

    :param body:
    :type body: V1MeetingsMeetingIdEnrollApprovalsPutRequest
    """  # noqa: E501

    def __init__(
        self,
        meeting_id: str,
        body: Optional[V1MeetingsMeetingIdEnrollApprovalsPutRequest] = None
    ):
        self.meeting_id = meeting_id
        self.body = body


class ApiV1MeetingsMeetingIdEnrollApprovalsPutResponse(ApiResponse):
    data: Optional[V1MeetingsMeetingIdEnrollApprovalsPut200Response] = None

    def __init__(self, api_resp: ApiResponse, data: Optional[V1MeetingsMeetingIdEnrollApprovalsPut200Response] = None):
        super().__init__(
            status_code=api_resp.status_code,
            raw_body=api_resp.raw_body,
            header=api_resp.header,
            serializer=api_resp.serializer()
        )
        self.data = data


class ApiV1MeetingsMeetingIdEnrollConfigGetRequest(object):
    """查询会议报名配置

    查询云会议的报名配置和报名问题，仅会议创建者可查询。会议未开启报名时会返回未开启报名错误。 企业 secret 鉴权用户可查询任何该企业该用户创建的有效会议，OAuth2.0 鉴权用户只能查询通过 OAuth2.0 鉴权创建的有效会议。 用户必须是注册用户，请求头部 X-TC-Registered 字段必须传入为1。
    
    :param meeting_id: 会议ID (required)
    :type meeting_id: str

    :param instanceid: 用户的终端设备类型： 1：PC 2：Mac 3：Android 4：iOS 5：Web 6：iPad 7：Android Pad 8：小程序 (required)
    :type instanceid: str

    :param userid: 会议创建者的用户 ID（企业内部请使用企业唯一用户标识；OAuth2.0 鉴权用户请使用 openId）
    :type userid: str

    :param operator_id_type: 操作者 ID 的类型：  1: userid 2: open_id  如果operator_id和userid具有值，则以operator_id为准；
    :type operator_id_type: str

    :param operator_id: 操作者 ID。会议创建者可以导入报名信息。 operator_id 必须与 operator_id_type 配合使用。根据 operator_id_type 的值，operator_id 代表不同类型。  operator_id_type=2，operator_id必须和公共参数的openid一致。  operator_id和userid至少填写一个，两个参数如果都传了以operator_id为准。  使用OAuth公参鉴权后不能使用userid为入参。
    :type operator_id: str

    :param body:
    :type body: object
    """  # noqa: E501

    def __init__(
        self,
        meeting_id: str,
        instanceid: Optional[str] = None,
        userid: Optional[str] = None,
        operator_id_type: Optional[str] = None,
        operator_id: Optional[str] = None,
        body: Optional[object] = None
    ):
        self.meeting_id = meeting_id
        self.instanceid = instanceid
        self.userid = userid
        self.operator_id_type = operator_id_type
        self.operator_id = operator_id
        self.body = body


class ApiV1MeetingsMeetingIdEnrollConfigGetResponse(ApiResponse):
    data: Optional[V1MeetingsMeetingIdEnrollConfigGet200Response] = None

    def __init__(self, api_resp: ApiResponse, data: Optional[V1MeetingsMeetingIdEnrollConfigGet200Response] = None):
        super().__init__(
            status_code=api_resp.status_code,
            raw_body=api_resp.raw_body,
            header=api_resp.header,
            serializer=api_resp.serializer()
        )
        self.data = data


class ApiV1MeetingsMeetingIdEnrollConfigPutRequest(object):
    """修改会议报名配置

    修改云会议的报名配置和报名问题，仅会议创建者可修改，且需要会议已开启报名。 企业 secret 鉴权用户可修改任何该企业该用户创建的有效会议，OAuth2.0 鉴权用户只能修改通过 OAuth2.0 鉴权创建的有效会议。 用户必须是注册用户，请求头部 X-TC-Registered 字段必须传入为1。
    
    :param meeting_id: 会议ID (required)
    :type meeting_id: str

    :param body:
    :type body: V1MeetingsMeetingIdEnrollConfigPutRequest
    """  # noqa: E501

    def __init__(
        self,
        meeting_id: str,
        body: Optional[V1MeetingsMeetingIdEnrollConfigPutRequest] = None
    ):
        self.meeting_id = meeting_id
        self.body = body


class ApiV1MeetingsMeetingIdEnrollConfigPutResponse(ApiResponse):
    data: Optional[V1MeetingsMeetingIdEnrollConfigPut200Response] = None

    def __init__(self, api_resp: ApiResponse, data: Optional[V1MeetingsMeetingIdEnrollConfigPut200Response] = None):
        super().__init__(
            status_code=api_resp.status_code,
            raw_body=api_resp.raw_body,
            header=api_resp.header,
            serializer=api_resp.serializer()
        )
        self.data = data


class ApiV1MeetingsMeetingIdEnrollIdsPostRequest(object):
    """查询会议成员报名ID

    描述： 支持查询会议中已报名成员的报名 ID，仅会议创建者可查询。
    
    :param meeting_id: 会议ID (required)
    :type meeting_id: str

    :param body:
    :type body: V1MeetingsMeetingIdEnrollIdsPostRequest
    """  # noqa: E501

    def __init__(
        self,
        meeting_id: str,
        body: Optional[V1MeetingsMeetingIdEnrollIdsPostRequest] = None
    ):
        self.meeting_id = meeting_id
        self.body = body


class ApiV1MeetingsMeetingIdEnrollIdsPostResponse(ApiResponse):
    data: Optional[V1MeetingsMeetingIdEnrollIdsPost200Response] = None

    def __init__(self, api_resp: ApiResponse, data: Optional[V1MeetingsMeetingIdEnrollIdsPost200Response] = None):
        super().__init__(
            status_code=api_resp.status_code,
            raw_body=api_resp.raw_body,
            header=api_resp.header,
            serializer=api_resp.serializer()
        )
        self.data = data


class ApiV1MeetingsMeetingIdEnrollImportPostRequest(object):
    """导入会议报名信息

    指定会议中导入报名信息。  企业 secret 鉴权用户可通过同企业下用户 userid 和手机号导入报名信息，OAuth2.0 鉴权用户能通过用户 open_id，与应用同企业下的 userid 以及手机号导入报名信息。 用户必须是注册用户，请求头部 X-TC-Registered 字段必须传入为1。 商业版单场会议导入上限1000条，企业版单场会议导入上限4000条。如需提升，请联系我们。
    
    :param meeting_id: 会议id (required)
    :type meeting_id: str

    :param body:
    :type body: V1MeetingsMeetingIdEnrollImportPostRequest
    """  # noqa: E501

    def __init__(
        self,
        meeting_id: str,
        body: Optional[V1MeetingsMeetingIdEnrollImportPostRequest] = None
    ):
        self.meeting_id = meeting_id
        self.body = body


class ApiV1MeetingsMeetingIdEnrollImportPostResponse(ApiResponse):
    data: Optional[V1MeetingsMeetingIdEnrollImportPost200Response] = None

    def __init__(self, api_resp: ApiResponse, data: Optional[V1MeetingsMeetingIdEnrollImportPost200Response] = None):
        super().__init__(
            status_code=api_resp.status_code,
            raw_body=api_resp.raw_body,
            header=api_resp.header,
            serializer=api_resp.serializer()
        )
        self.data = data


class ApiV1MeetingsMeetingIdEnrollUnregistrationDeleteRequest(object):
    """删除会议报名信息

    描述： 删除指定会议的报名信息，支持删除用户手动报名的信息和导入的报名信息。 企业 secret 鉴权用户可删除该用户企业会议下的报名信息，OAuth2.0 鉴权用户只能删除通过 OAuth2.0 鉴权创建的有效会议的报名信息。 用户必须是注册用户，请求头部 X-TC-Registered 字段必须传入为1。
    
    :param meeting_id: (required)
    :type meeting_id: str

    :param body:
    :type body: V1MeetingsMeetingIdEnrollUnregistrationDeleteRequest
    """  # noqa: E501

    def __init__(
        self,
        meeting_id: str,
        body: Optional[V1MeetingsMeetingIdEnrollUnregistrationDeleteRequest] = None
    ):
        self.meeting_id = meeting_id
        self.body = body


class ApiV1MeetingsMeetingIdEnrollUnregistrationDeleteResponse(ApiResponse):
    data: Optional[V1MeetingsMeetingIdEnrollUnregistrationDelete200Response] = None

    def __init__(self, api_resp: ApiResponse, data: Optional[V1MeetingsMeetingIdEnrollUnregistrationDelete200Response] = None):
        super().__init__(
            status_code=api_resp.status_code,
            raw_body=api_resp.raw_body,
            header=api_resp.header,
            serializer=api_resp.serializer()
        )
        self.data = data


class ApiV1MeetingsMeetingIdGetRequest(object):
    """通过会议ID查询会议列表

    通过会议 ID 查询会议详情。 企业 secret 鉴权用户可查询到任何该用户创建的企业下的会议，OAuth2.0 鉴权用户只能查询到通过 OAuth2.0 鉴权创建的会议。 本接口的邀请参会成员限制调整至300人。 当会议为周期性会议时，主持人密钥每场会议固定，但单场会议只能获取一次。支持查询周期性会议的主持人密钥。 支持查询 MRA 当前所在会议信息。
    
    :param meeting_id: (required)
    :type meeting_id: str

    :param instanceid: 用户的终端设备类型： 0：PSTN 1：PC 2：Mac 3：Android 4：iOS 5：Web 6：iPad 7：Android Pad 8：小程序 9：voip、sip 设备 10：linux 20：Rooms for Touch Windows 21：Rooms for Touch MacOS 22：Rooms for Touch Android 30：Controller for Touch Windows 32：Controller for Touch Android 33：Controller for Touch iOS (required)
    :type instanceid: str

    :param userid: 会议创建者的用户 ID（企业内部请使用企业唯一用户标识；OAuth2.0 鉴权用户请使用 openId）
    :type userid: str

    :param operator_id: 操作者ID，根据operator_id_type的值，使用不同的类型
    :type operator_id: str

    :param operator_id_type: 操作者ID的类型：1.userid 2.openid 3.rooms_id
    :type operator_id_type: str

    :param body:
    :type body: object
    """  # noqa: E501

    def __init__(
        self,
        meeting_id: str,
        instanceid: Optional[str] = None,
        userid: Optional[str] = None,
        operator_id: Optional[str] = None,
        operator_id_type: Optional[str] = None,
        body: Optional[object] = None
    ):
        self.meeting_id = meeting_id
        self.instanceid = instanceid
        self.userid = userid
        self.operator_id = operator_id
        self.operator_id_type = operator_id_type
        self.body = body


class ApiV1MeetingsMeetingIdGetResponse(ApiResponse):
    data: Optional[V1MeetingsMeetingIdGet200Response] = None

    def __init__(self, api_resp: ApiResponse, data: Optional[V1MeetingsMeetingIdGet200Response] = None):
        super().__init__(
            status_code=api_resp.status_code,
            raw_body=api_resp.raw_body,
            header=api_resp.header,
            serializer=api_resp.serializer()
        )
        self.data = data


class ApiV1MeetingsMeetingIdPutRequest(object):
    """修改会议

    修改某指定会议的会议信息。  企业 secret 鉴权用户可修改任何该企业该用户创建的有效会议，OAuth2.0 鉴权用户只能修改通过 OAuth2.0 鉴权创建的有效会议。 当您想实时监测会议修改状况时，您可以通过订阅 [会议更新](https://cloud.tencent.com/document/product/1095/51615) 的事件，接收事件通知。 本接口的邀请参会成员限制调整至300人。 当会议为周期性会议时，主持人密钥每场会议固定，但单场会议只能获取一次。支持修改周期性会议的主持人密钥。
    
    :param meeting_id: (required)
    :type meeting_id: str

    :param body:
    :type body: V1MeetingsMeetingIdPutRequest
    """  # noqa: E501

    def __init__(
        self,
        meeting_id: str,
        body: Optional[V1MeetingsMeetingIdPutRequest] = None
    ):
        self.meeting_id = meeting_id
        self.body = body


class ApiV1MeetingsMeetingIdPutResponse(ApiResponse):
    data: Optional[V1MeetingsMeetingIdPut200Response] = None

    def __init__(self, api_resp: ApiResponse, data: Optional[V1MeetingsMeetingIdPut200Response] = None):
        super().__init__(
            status_code=api_resp.status_code,
            raw_body=api_resp.raw_body,
            header=api_resp.header,
            serializer=api_resp.serializer()
        )
        self.data = data


class ApiV1MeetingsPostRequest(object):
    """创建会议

    快速创建或预定一个会议。  企业 secret 鉴权用户可创建该用户所属企业下的会议，OAuth2.0 鉴权用户只能创建该企业下 OAuth2.0 应用的会议。 用户必须是注册用户，请求头部 X-TC-Registered 字段必须传入为1。 当您想实时监测会议创建状况时，您可以通过订阅 [会议创建](https://cloud.tencent.com/document/product/1095/51614) 的事件，接收事件通知。 本接口的邀请参会成员限制调整至300人。 当会议为周期性会议时，主持人密钥每场会议固定，但单场会议只能获取一次。支持创建周期性会议的主持人密钥。
    
    :param body:
    :type body: V1MeetingsPostRequest
    """  # noqa: E501

    def __init__(
        self,
        body: Optional[V1MeetingsPostRequest] = None
    ):
        self.body = body


class ApiV1MeetingsPostResponse(ApiResponse):
    data: Optional[V1MeetingsPost200Response] = None

    def __init__(self, api_resp: ApiResponse, data: Optional[V1MeetingsPost200Response] = None):
        super().__init__(
            status_code=api_resp.status_code,
            raw_body=api_resp.raw_body,
            header=api_resp.header,
            serializer=api_resp.serializer()
        )
        self.data = data


class MeetingsApi:
    def __init__(self, config: Config):
        self.__config = config

    def v1_meeting_set_waiting_room_welcome_message_post(
        self,
        request: ApiV1MeetingSetWaitingRoomWelcomeMessagePostRequest,
        serializer: Optional[Serializer] = None,
        authenticator_options: Optional[List[Callable[[Config], Authenticator]]] = None,
        header: Optional[Dict[str, str]] = None
    ) -> ApiV1MeetingSetWaitingRoomWelcomeMessagePostResponse:
        """v1_meeting_set_waiting_room_welcome_message_post 设置等候室欢迎语[/v1/meeting/set-waiting-room-welcome-message - POST]

            为已开启等候室的会议配置等候室欢迎语。当有用户进入等候室时，会收到来自会议主办方的私聊消息引导。  鉴权方式: JWT鉴权、OAuth鉴权
        """
        try:
            # 生成鉴权器
            authenticators: List[Authenticator] = []
            for option in authenticator_options:
                authenticators.append(option(self.__config))

            # 增加 SDK Version 标识
            authenticators.append(DEFAULT_AUTHENTICATOR)
            # 构造请求
            api_req = ApiRequest(api_uri="/v1/meeting/set-waiting-room-welcome-message",
                                 authenticators=authenticators,
                                 header=header, 
                                 body=request.body,
                                 serializer=serializer)
            # path 参数
            # query 参数
            # 发送请求
            api_resp = self.__config.clt.post(api_req)

            if api_resp.status_code >= 300:
                raise ServiceException(api_resp=api_resp)
            try:
                response = ApiV1MeetingSetWaitingRoomWelcomeMessagePostResponse(api_resp=api_resp)
                response.data = api_resp.translate(dst_t=V1MeetingSetWaitingRoomWelcomeMessagePost200Response)
            except Exception as e:
                raise ClientException(Exception(f"http status code: {api_resp.status_code}, "
                                                f"response: {api_resp.raw_body}, err: {e.__str__()}"))
            return response
        except (ClientException, ServiceException):
            raise
        except Exception as e:
            raise ClientException(e)

    def v1_meetings_get(
        self,
        request: ApiV1MeetingsGetRequest,
        serializer: Optional[Serializer] = None,
        authenticator_options: Optional[List[Callable[[Config], Authenticator]]] = None,
        header: Optional[Dict[str, str]] = None
    ) -> ApiV1MeetingsGetResponse:
        """v1_meetings_get 通过会议CODE查询会议列表[/v1/meetings - GET]

            通过会议 ID 查询会议详情。 企业 secret 鉴权用户可查询到任何该用户创建的企业下的会议，OAuth2.0 鉴权用户只能查询到通过 OAuth2.0 鉴权创建的会议。 支持企业管理员查询企业下的会议。 本接口的邀请参会成员限制调整至300人。 当会议为周期性会议时，主持人密钥每场会议固定，但单场会议只能获取一次。支持查询周期性会议的主持人密钥。 支持查询 MRA 当前所在会议信息。 若会议号被回收则无法通过 Code 查询，您可以通过会议 ID 查询到该会议。
        """
        try:
            # 生成鉴权器
            authenticators: List[Authenticator] = []
            for option in authenticator_options:
                authenticators.append(option(self.__config))

            # 增加 SDK Version 标识
            authenticators.append(DEFAULT_AUTHENTICATOR)
            # 构造请求
            api_req = ApiRequest(api_uri="/v1/meetings",
                                 authenticators=authenticators,
                                 header=header, 
                                 body=request.body,
                                 serializer=serializer)
            # path 参数
            # query 参数
            if request.operator_id is not None:
                api_req.query_params.append(('operator_id', request.operator_id))
            if request.operator_id_type is not None:
                api_req.query_params.append(('operator_id_type', request.operator_id_type))
            if request.userid is not None:
                api_req.query_params.append(('userid', request.userid))
            if request.instanceid is not None:
                api_req.query_params.append(('instanceid', request.instanceid))
            if request.meeting_code is not None:
                api_req.query_params.append(('meeting_code', request.meeting_code))
            if request.cursory is not None:
                api_req.query_params.append(('cursory', request.cursory))
            if request.pos is not None:
                api_req.query_params.append(('pos', request.pos))
            if request.is_show_all_sub_meetings is not None:
                api_req.query_params.append(('is_show_all_sub_meetings', request.is_show_all_sub_meetings))
            # 发送请求
            api_resp = self.__config.clt.get(api_req)

            if api_resp.status_code >= 300:
                raise ServiceException(api_resp=api_resp)
            try:
                response = ApiV1MeetingsGetResponse(api_resp=api_resp)
                response.data = api_resp.translate(dst_t=V1MeetingsGet200Response)
            except Exception as e:
                raise ClientException(Exception(f"http status code: {api_resp.status_code}, "
                                                f"response: {api_resp.raw_body}, err: {e.__str__()}"))
            return response
        except (ClientException, ServiceException):
            raise
        except Exception as e:
            raise ClientException(e)

    def v1_meetings_meeting_id_cancel_post(
        self,
        request: ApiV1MeetingsMeetingIdCancelPostRequest,
        serializer: Optional[Serializer] = None,
        authenticator_options: Optional[List[Callable[[Config], Authenticator]]] = None,
        header: Optional[Dict[str, str]] = None
    ) -> ApiV1MeetingsMeetingIdCancelPostResponse:
        """v1_meetings_meeting_id_cancel_post 取消会议[/v1/meetings/{meeting_id}/cancel - POST]

            取消用户创建的会议。用户只能取消自己创建的会议，且该会议是一个有效的会议。如果不是会议创建者或者无效会议号将会返回错误。 企业 secret 鉴权用户可取消任何该用户企业下创建的有效会议，OAuth2.0 鉴权用户只能取消通过 OAuth2.0 鉴权创建的有效会议。 当您想实时监测会议取消状况时，您可以通过订阅 [会议取消](https://cloud.tencent.com/document/product/1095/51616) 的事件，接收事件通知。
        """
        try:
            # 生成鉴权器
            authenticators: List[Authenticator] = []
            for option in authenticator_options:
                authenticators.append(option(self.__config))

            # 增加 SDK Version 标识
            authenticators.append(DEFAULT_AUTHENTICATOR)
            # 构造请求
            api_req = ApiRequest(api_uri="/v1/meetings/{meeting_id}/cancel",
                                 authenticators=authenticators,
                                 header=header, 
                                 body=request.body,
                                 serializer=serializer)
            # path 参数
            if request.meeting_id is not None:
                api_req.path_params['meeting_id'] = request.meeting_id
            # query 参数
            # 发送请求
            api_resp = self.__config.clt.post(api_req)

            if api_resp.status_code >= 300:
                raise ServiceException(api_resp=api_resp)
            try:
                response = ApiV1MeetingsMeetingIdCancelPostResponse(api_resp=api_resp)
                response.data = api_resp.translate(dst_t=object)
            except Exception as e:
                raise ClientException(Exception(f"http status code: {api_resp.status_code}, "
                                                f"response: {api_resp.raw_body}, err: {e.__str__()}"))
            return response
        except (ClientException, ServiceException):
            raise
        except Exception as e:
            raise ClientException(e)

    def v1_meetings_meeting_id_enroll_approvals_get(
        self,
        request: ApiV1MeetingsMeetingIdEnrollApprovalsGetRequest,
        serializer: Optional[Serializer] = None,
        authenticator_options: Optional[List[Callable[[Config], Authenticator]]] = None,
        header: Optional[Dict[str, str]] = None
    ) -> ApiV1MeetingsMeetingIdEnrollApprovalsGetResponse:
        """v1_meetings_meeting_id_enroll_approvals_get 查询会议报名信息[/v1/meetings/{meeting_id}/enroll/approvals - GET]

            查询已报名观众数量和报名观众答题详情，仅会议创建者可查询。 企业 secret 鉴权用户可修改任何该企业该用户创建的有效会议，OAuth2.0 鉴权用户只能修改通过 OAuth2.0 鉴权创建的有效会议。 用户必须是注册用户，请求头部 X-TC-Registered 字段必须传入为1。
        """
        try:
            # 生成鉴权器
            authenticators: List[Authenticator] = []
            for option in authenticator_options:
                authenticators.append(option(self.__config))

            # 增加 SDK Version 标识
            authenticators.append(DEFAULT_AUTHENTICATOR)
            # 构造请求
            api_req = ApiRequest(api_uri="/v1/meetings/{meeting_id}/enroll/approvals",
                                 authenticators=authenticators,
                                 header=header, 
                                 body=request.body,
                                 serializer=serializer)
            # path 参数
            if request.meeting_id is not None:
                api_req.path_params['meeting_id'] = request.meeting_id
            # query 参数
            if request.userid is not None:
                api_req.query_params.append(('userid', request.userid))
            if request.instanceid is not None:
                api_req.query_params.append(('instanceid', request.instanceid))
            if request.page is not None:
                api_req.query_params.append(('page', request.page))
            if request.page_size is not None:
                api_req.query_params.append(('page_size', request.page_size))
            if request.status is not None:
                api_req.query_params.append(('status', request.status))
            if request.operator_id is not None:
                api_req.query_params.append(('operator_id', request.operator_id))
            if request.operator_id_type is not None:
                api_req.query_params.append(('operator_id_type', request.operator_id_type))
            # 发送请求
            api_resp = self.__config.clt.get(api_req)

            if api_resp.status_code >= 300:
                raise ServiceException(api_resp=api_resp)
            try:
                response = ApiV1MeetingsMeetingIdEnrollApprovalsGetResponse(api_resp=api_resp)
                response.data = api_resp.translate(dst_t=V1MeetingsMeetingIdEnrollApprovalsGet200Response)
            except Exception as e:
                raise ClientException(Exception(f"http status code: {api_resp.status_code}, "
                                                f"response: {api_resp.raw_body}, err: {e.__str__()}"))
            return response
        except (ClientException, ServiceException):
            raise
        except Exception as e:
            raise ClientException(e)

    def v1_meetings_meeting_id_enroll_approvals_put(
        self,
        request: ApiV1MeetingsMeetingIdEnrollApprovalsPutRequest,
        serializer: Optional[Serializer] = None,
        authenticator_options: Optional[List[Callable[[Config], Authenticator]]] = None,
        header: Optional[Dict[str, str]] = None
    ) -> ApiV1MeetingsMeetingIdEnrollApprovalsPutResponse:
        """v1_meetings_meeting_id_enroll_approvals_put 审批云会议报名信息[/v1/meetings/{meeting_id}/enroll/approvals - PUT]

            批量云会议的报名信息，仅会议创建者可审批。 企业 secret 鉴权用户可审批任何该企业该用户创建的有效会议，OAuth2.0 鉴权用户只能审批通过 OAuth2.0 鉴权创建的有效会议。 用户必须是注册用户，请求头部 X-TC-Registered 字段必须传入为1。
        """
        try:
            # 生成鉴权器
            authenticators: List[Authenticator] = []
            for option in authenticator_options:
                authenticators.append(option(self.__config))

            # 增加 SDK Version 标识
            authenticators.append(DEFAULT_AUTHENTICATOR)
            # 构造请求
            api_req = ApiRequest(api_uri="/v1/meetings/{meeting_id}/enroll/approvals",
                                 authenticators=authenticators,
                                 header=header, 
                                 body=request.body,
                                 serializer=serializer)
            # path 参数
            if request.meeting_id is not None:
                api_req.path_params['meeting_id'] = request.meeting_id
            # query 参数
            # 发送请求
            api_resp = self.__config.clt.put(api_req)

            if api_resp.status_code >= 300:
                raise ServiceException(api_resp=api_resp)
            try:
                response = ApiV1MeetingsMeetingIdEnrollApprovalsPutResponse(api_resp=api_resp)
                response.data = api_resp.translate(dst_t=V1MeetingsMeetingIdEnrollApprovalsPut200Response)
            except Exception as e:
                raise ClientException(Exception(f"http status code: {api_resp.status_code}, "
                                                f"response: {api_resp.raw_body}, err: {e.__str__()}"))
            return response
        except (ClientException, ServiceException):
            raise
        except Exception as e:
            raise ClientException(e)

    def v1_meetings_meeting_id_enroll_config_get(
        self,
        request: ApiV1MeetingsMeetingIdEnrollConfigGetRequest,
        serializer: Optional[Serializer] = None,
        authenticator_options: Optional[List[Callable[[Config], Authenticator]]] = None,
        header: Optional[Dict[str, str]] = None
    ) -> ApiV1MeetingsMeetingIdEnrollConfigGetResponse:
        """v1_meetings_meeting_id_enroll_config_get 查询会议报名配置[/v1/meetings/{meeting_id}/enroll/config - GET]

            查询云会议的报名配置和报名问题，仅会议创建者可查询。会议未开启报名时会返回未开启报名错误。 企业 secret 鉴权用户可查询任何该企业该用户创建的有效会议，OAuth2.0 鉴权用户只能查询通过 OAuth2.0 鉴权创建的有效会议。 用户必须是注册用户，请求头部 X-TC-Registered 字段必须传入为1。
        """
        try:
            # 生成鉴权器
            authenticators: List[Authenticator] = []
            for option in authenticator_options:
                authenticators.append(option(self.__config))

            # 增加 SDK Version 标识
            authenticators.append(DEFAULT_AUTHENTICATOR)
            # 构造请求
            api_req = ApiRequest(api_uri="/v1/meetings/{meeting_id}/enroll/config",
                                 authenticators=authenticators,
                                 header=header, 
                                 body=request.body,
                                 serializer=serializer)
            # path 参数
            if request.meeting_id is not None:
                api_req.path_params['meeting_id'] = request.meeting_id
            # query 参数
            if request.userid is not None:
                api_req.query_params.append(('userid', request.userid))
            if request.instanceid is not None:
                api_req.query_params.append(('instanceid', request.instanceid))
            if request.operator_id_type is not None:
                api_req.query_params.append(('operator_id_type', request.operator_id_type))
            if request.operator_id is not None:
                api_req.query_params.append(('operator_id', request.operator_id))
            # 发送请求
            api_resp = self.__config.clt.get(api_req)

            if api_resp.status_code >= 300:
                raise ServiceException(api_resp=api_resp)
            try:
                response = ApiV1MeetingsMeetingIdEnrollConfigGetResponse(api_resp=api_resp)
                response.data = api_resp.translate(dst_t=V1MeetingsMeetingIdEnrollConfigGet200Response)
            except Exception as e:
                raise ClientException(Exception(f"http status code: {api_resp.status_code}, "
                                                f"response: {api_resp.raw_body}, err: {e.__str__()}"))
            return response
        except (ClientException, ServiceException):
            raise
        except Exception as e:
            raise ClientException(e)

    def v1_meetings_meeting_id_enroll_config_put(
        self,
        request: ApiV1MeetingsMeetingIdEnrollConfigPutRequest,
        serializer: Optional[Serializer] = None,
        authenticator_options: Optional[List[Callable[[Config], Authenticator]]] = None,
        header: Optional[Dict[str, str]] = None
    ) -> ApiV1MeetingsMeetingIdEnrollConfigPutResponse:
        """v1_meetings_meeting_id_enroll_config_put 修改会议报名配置[/v1/meetings/{meeting_id}/enroll/config - PUT]

            修改云会议的报名配置和报名问题，仅会议创建者可修改，且需要会议已开启报名。 企业 secret 鉴权用户可修改任何该企业该用户创建的有效会议，OAuth2.0 鉴权用户只能修改通过 OAuth2.0 鉴权创建的有效会议。 用户必须是注册用户，请求头部 X-TC-Registered 字段必须传入为1。
        """
        try:
            # 生成鉴权器
            authenticators: List[Authenticator] = []
            for option in authenticator_options:
                authenticators.append(option(self.__config))

            # 增加 SDK Version 标识
            authenticators.append(DEFAULT_AUTHENTICATOR)
            # 构造请求
            api_req = ApiRequest(api_uri="/v1/meetings/{meeting_id}/enroll/config",
                                 authenticators=authenticators,
                                 header=header, 
                                 body=request.body,
                                 serializer=serializer)
            # path 参数
            if request.meeting_id is not None:
                api_req.path_params['meeting_id'] = request.meeting_id
            # query 参数
            # 发送请求
            api_resp = self.__config.clt.put(api_req)

            if api_resp.status_code >= 300:
                raise ServiceException(api_resp=api_resp)
            try:
                response = ApiV1MeetingsMeetingIdEnrollConfigPutResponse(api_resp=api_resp)
                response.data = api_resp.translate(dst_t=V1MeetingsMeetingIdEnrollConfigPut200Response)
            except Exception as e:
                raise ClientException(Exception(f"http status code: {api_resp.status_code}, "
                                                f"response: {api_resp.raw_body}, err: {e.__str__()}"))
            return response
        except (ClientException, ServiceException):
            raise
        except Exception as e:
            raise ClientException(e)

    def v1_meetings_meeting_id_enroll_ids_post(
        self,
        request: ApiV1MeetingsMeetingIdEnrollIdsPostRequest,
        serializer: Optional[Serializer] = None,
        authenticator_options: Optional[List[Callable[[Config], Authenticator]]] = None,
        header: Optional[Dict[str, str]] = None
    ) -> ApiV1MeetingsMeetingIdEnrollIdsPostResponse:
        """v1_meetings_meeting_id_enroll_ids_post 查询会议成员报名ID[/v1/meetings/{meeting_id}/enroll/ids - POST]

            描述： 支持查询会议中已报名成员的报名 ID，仅会议创建者可查询。
        """
        try:
            # 生成鉴权器
            authenticators: List[Authenticator] = []
            for option in authenticator_options:
                authenticators.append(option(self.__config))

            # 增加 SDK Version 标识
            authenticators.append(DEFAULT_AUTHENTICATOR)
            # 构造请求
            api_req = ApiRequest(api_uri="/v1/meetings/{meeting_id}/enroll/ids",
                                 authenticators=authenticators,
                                 header=header, 
                                 body=request.body,
                                 serializer=serializer)
            # path 参数
            if request.meeting_id is not None:
                api_req.path_params['meeting_id'] = request.meeting_id
            # query 参数
            # 发送请求
            api_resp = self.__config.clt.post(api_req)

            if api_resp.status_code >= 300:
                raise ServiceException(api_resp=api_resp)
            try:
                response = ApiV1MeetingsMeetingIdEnrollIdsPostResponse(api_resp=api_resp)
                response.data = api_resp.translate(dst_t=V1MeetingsMeetingIdEnrollIdsPost200Response)
            except Exception as e:
                raise ClientException(Exception(f"http status code: {api_resp.status_code}, "
                                                f"response: {api_resp.raw_body}, err: {e.__str__()}"))
            return response
        except (ClientException, ServiceException):
            raise
        except Exception as e:
            raise ClientException(e)

    def v1_meetings_meeting_id_enroll_import_post(
        self,
        request: ApiV1MeetingsMeetingIdEnrollImportPostRequest,
        serializer: Optional[Serializer] = None,
        authenticator_options: Optional[List[Callable[[Config], Authenticator]]] = None,
        header: Optional[Dict[str, str]] = None
    ) -> ApiV1MeetingsMeetingIdEnrollImportPostResponse:
        """v1_meetings_meeting_id_enroll_import_post 导入会议报名信息[/v1/meetings/{meeting_id}/enroll/import - POST]

            指定会议中导入报名信息。  企业 secret 鉴权用户可通过同企业下用户 userid 和手机号导入报名信息，OAuth2.0 鉴权用户能通过用户 open_id，与应用同企业下的 userid 以及手机号导入报名信息。 用户必须是注册用户，请求头部 X-TC-Registered 字段必须传入为1。 商业版单场会议导入上限1000条，企业版单场会议导入上限4000条。如需提升，请联系我们。
        """
        try:
            # 生成鉴权器
            authenticators: List[Authenticator] = []
            for option in authenticator_options:
                authenticators.append(option(self.__config))

            # 增加 SDK Version 标识
            authenticators.append(DEFAULT_AUTHENTICATOR)
            # 构造请求
            api_req = ApiRequest(api_uri="/v1/meetings/{meeting_id}/enroll/import",
                                 authenticators=authenticators,
                                 header=header, 
                                 body=request.body,
                                 serializer=serializer)
            # path 参数
            if request.meeting_id is not None:
                api_req.path_params['meeting_id'] = request.meeting_id
            # query 参数
            # 发送请求
            api_resp = self.__config.clt.post(api_req)

            if api_resp.status_code >= 300:
                raise ServiceException(api_resp=api_resp)
            try:
                response = ApiV1MeetingsMeetingIdEnrollImportPostResponse(api_resp=api_resp)
                response.data = api_resp.translate(dst_t=V1MeetingsMeetingIdEnrollImportPost200Response)
            except Exception as e:
                raise ClientException(Exception(f"http status code: {api_resp.status_code}, "
                                                f"response: {api_resp.raw_body}, err: {e.__str__()}"))
            return response
        except (ClientException, ServiceException):
            raise
        except Exception as e:
            raise ClientException(e)

    def v1_meetings_meeting_id_enroll_unregistration_delete(
        self,
        request: ApiV1MeetingsMeetingIdEnrollUnregistrationDeleteRequest,
        serializer: Optional[Serializer] = None,
        authenticator_options: Optional[List[Callable[[Config], Authenticator]]] = None,
        header: Optional[Dict[str, str]] = None
    ) -> ApiV1MeetingsMeetingIdEnrollUnregistrationDeleteResponse:
        """v1_meetings_meeting_id_enroll_unregistration_delete 删除会议报名信息[/v1/meetings/{meeting_id}/enroll/unregistration - DELETE]

            描述： 删除指定会议的报名信息，支持删除用户手动报名的信息和导入的报名信息。 企业 secret 鉴权用户可删除该用户企业会议下的报名信息，OAuth2.0 鉴权用户只能删除通过 OAuth2.0 鉴权创建的有效会议的报名信息。 用户必须是注册用户，请求头部 X-TC-Registered 字段必须传入为1。
        """
        try:
            # 生成鉴权器
            authenticators: List[Authenticator] = []
            for option in authenticator_options:
                authenticators.append(option(self.__config))

            # 增加 SDK Version 标识
            authenticators.append(DEFAULT_AUTHENTICATOR)
            # 构造请求
            api_req = ApiRequest(api_uri="/v1/meetings/{meeting_id}/enroll/unregistration",
                                 authenticators=authenticators,
                                 header=header, 
                                 body=request.body,
                                 serializer=serializer)
            # path 参数
            if request.meeting_id is not None:
                api_req.path_params['meeting_id'] = request.meeting_id
            # query 参数
            # 发送请求
            api_resp = self.__config.clt.delete(api_req)

            if api_resp.status_code >= 300:
                raise ServiceException(api_resp=api_resp)
            try:
                response = ApiV1MeetingsMeetingIdEnrollUnregistrationDeleteResponse(api_resp=api_resp)
                response.data = api_resp.translate(dst_t=V1MeetingsMeetingIdEnrollUnregistrationDelete200Response)
            except Exception as e:
                raise ClientException(Exception(f"http status code: {api_resp.status_code}, "
                                                f"response: {api_resp.raw_body}, err: {e.__str__()}"))
            return response
        except (ClientException, ServiceException):
            raise
        except Exception as e:
            raise ClientException(e)

    def v1_meetings_meeting_id_get(
        self,
        request: ApiV1MeetingsMeetingIdGetRequest,
        serializer: Optional[Serializer] = None,
        authenticator_options: Optional[List[Callable[[Config], Authenticator]]] = None,
        header: Optional[Dict[str, str]] = None
    ) -> ApiV1MeetingsMeetingIdGetResponse:
        """v1_meetings_meeting_id_get 通过会议ID查询会议列表[/v1/meetings/{meeting_id} - GET]

            通过会议 ID 查询会议详情。 企业 secret 鉴权用户可查询到任何该用户创建的企业下的会议，OAuth2.0 鉴权用户只能查询到通过 OAuth2.0 鉴权创建的会议。 本接口的邀请参会成员限制调整至300人。 当会议为周期性会议时，主持人密钥每场会议固定，但单场会议只能获取一次。支持查询周期性会议的主持人密钥。 支持查询 MRA 当前所在会议信息。
        """
        try:
            # 生成鉴权器
            authenticators: List[Authenticator] = []
            for option in authenticator_options:
                authenticators.append(option(self.__config))

            # 增加 SDK Version 标识
            authenticators.append(DEFAULT_AUTHENTICATOR)
            # 构造请求
            api_req = ApiRequest(api_uri="/v1/meetings/{meeting_id}",
                                 authenticators=authenticators,
                                 header=header, 
                                 body=request.body,
                                 serializer=serializer)
            # path 参数
            if request.meeting_id is not None:
                api_req.path_params['meeting_id'] = request.meeting_id
            # query 参数
            if request.userid is not None:
                api_req.query_params.append(('userid', request.userid))
            if request.instanceid is not None:
                api_req.query_params.append(('instanceid', request.instanceid))
            if request.operator_id is not None:
                api_req.query_params.append(('operator_id', request.operator_id))
            if request.operator_id_type is not None:
                api_req.query_params.append(('operator_id_type', request.operator_id_type))
            # 发送请求
            api_resp = self.__config.clt.get(api_req)

            if api_resp.status_code >= 300:
                raise ServiceException(api_resp=api_resp)
            try:
                response = ApiV1MeetingsMeetingIdGetResponse(api_resp=api_resp)
                response.data = api_resp.translate(dst_t=V1MeetingsMeetingIdGet200Response)
            except Exception as e:
                raise ClientException(Exception(f"http status code: {api_resp.status_code}, "
                                                f"response: {api_resp.raw_body}, err: {e.__str__()}"))
            return response
        except (ClientException, ServiceException):
            raise
        except Exception as e:
            raise ClientException(e)

    def v1_meetings_meeting_id_put(
        self,
        request: ApiV1MeetingsMeetingIdPutRequest,
        serializer: Optional[Serializer] = None,
        authenticator_options: Optional[List[Callable[[Config], Authenticator]]] = None,
        header: Optional[Dict[str, str]] = None
    ) -> ApiV1MeetingsMeetingIdPutResponse:
        """v1_meetings_meeting_id_put 修改会议[/v1/meetings/{meeting_id} - PUT]

            修改某指定会议的会议信息。  企业 secret 鉴权用户可修改任何该企业该用户创建的有效会议，OAuth2.0 鉴权用户只能修改通过 OAuth2.0 鉴权创建的有效会议。 当您想实时监测会议修改状况时，您可以通过订阅 [会议更新](https://cloud.tencent.com/document/product/1095/51615) 的事件，接收事件通知。 本接口的邀请参会成员限制调整至300人。 当会议为周期性会议时，主持人密钥每场会议固定，但单场会议只能获取一次。支持修改周期性会议的主持人密钥。
        """
        try:
            # 生成鉴权器
            authenticators: List[Authenticator] = []
            for option in authenticator_options:
                authenticators.append(option(self.__config))

            # 增加 SDK Version 标识
            authenticators.append(DEFAULT_AUTHENTICATOR)
            # 构造请求
            api_req = ApiRequest(api_uri="/v1/meetings/{meeting_id}",
                                 authenticators=authenticators,
                                 header=header, 
                                 body=request.body,
                                 serializer=serializer)
            # path 参数
            if request.meeting_id is not None:
                api_req.path_params['meeting_id'] = request.meeting_id
            # query 参数
            # 发送请求
            api_resp = self.__config.clt.put(api_req)

            if api_resp.status_code >= 300:
                raise ServiceException(api_resp=api_resp)
            try:
                response = ApiV1MeetingsMeetingIdPutResponse(api_resp=api_resp)
                response.data = api_resp.translate(dst_t=V1MeetingsMeetingIdPut200Response)
            except Exception as e:
                raise ClientException(Exception(f"http status code: {api_resp.status_code}, "
                                                f"response: {api_resp.raw_body}, err: {e.__str__()}"))
            return response
        except (ClientException, ServiceException):
            raise
        except Exception as e:
            raise ClientException(e)

    def v1_meetings_post(
        self,
        request: ApiV1MeetingsPostRequest,
        serializer: Optional[Serializer] = None,
        authenticator_options: Optional[List[Callable[[Config], Authenticator]]] = None,
        header: Optional[Dict[str, str]] = None
    ) -> ApiV1MeetingsPostResponse:
        """v1_meetings_post 创建会议[/v1/meetings - POST]

            快速创建或预定一个会议。  企业 secret 鉴权用户可创建该用户所属企业下的会议，OAuth2.0 鉴权用户只能创建该企业下 OAuth2.0 应用的会议。 用户必须是注册用户，请求头部 X-TC-Registered 字段必须传入为1。 当您想实时监测会议创建状况时，您可以通过订阅 [会议创建](https://cloud.tencent.com/document/product/1095/51614) 的事件，接收事件通知。 本接口的邀请参会成员限制调整至300人。 当会议为周期性会议时，主持人密钥每场会议固定，但单场会议只能获取一次。支持创建周期性会议的主持人密钥。
        """
        try:
            # 生成鉴权器
            authenticators: List[Authenticator] = []
            for option in authenticator_options:
                authenticators.append(option(self.__config))

            # 增加 SDK Version 标识
            authenticators.append(DEFAULT_AUTHENTICATOR)
            # 构造请求
            api_req = ApiRequest(api_uri="/v1/meetings",
                                 authenticators=authenticators,
                                 header=header, 
                                 body=request.body,
                                 serializer=serializer)
            # path 参数
            # query 参数
            # 发送请求
            api_resp = self.__config.clt.post(api_req)

            if api_resp.status_code >= 300:
                raise ServiceException(api_resp=api_resp)
            try:
                response = ApiV1MeetingsPostResponse(api_resp=api_resp)
                response.data = api_resp.translate(dst_t=V1MeetingsPost200Response)
            except Exception as e:
                raise ClientException(Exception(f"http status code: {api_resp.status_code}, "
                                                f"response: {api_resp.raw_body}, err: {e.__str__()}"))
            return response
        except (ClientException, ServiceException):
            raise
        except Exception as e:
            raise ClientException(e)
