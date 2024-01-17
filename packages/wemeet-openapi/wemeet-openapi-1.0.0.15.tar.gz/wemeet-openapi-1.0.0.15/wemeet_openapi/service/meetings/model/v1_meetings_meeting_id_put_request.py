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
from wemeet_openapi.service.meetings.model.v1_meetings_post_request_guests_inner import V1MeetingsPostRequestGuestsInner
from wemeet_openapi.service.meetings.model.v1_meetings_meeting_id_put_request_hosts_inner import V1MeetingsMeetingIdPutRequestHostsInner
from wemeet_openapi.service.meetings.model.v1_meetings_post_request_invitees_inner import V1MeetingsPostRequestInviteesInner
from wemeet_openapi.service.meetings.model.v1_meetings_meeting_id_put_request_live_config import V1MeetingsMeetingIdPutRequestLiveConfig
from wemeet_openapi.service.meetings.model.v1_meetings_meeting_id_put_request_recurring_rule import V1MeetingsMeetingIdPutRequestRecurringRule
from wemeet_openapi.service.meetings.model.v1_meetings_meeting_id_put_request_settings import V1MeetingsMeetingIdPutRequestSettings


class V1MeetingsMeetingIdPutRequest(object):
    """V1MeetingsMeetingIdPutRequest

    :param enable_doc_upload_permission: 是否允许成员上传文档，默认为允许 
    :type enable_doc_upload_permission: Optional[bool]

    :param enable_enroll: 是否开启报名开关，默认不开启 
    :type enable_enroll: Optional[bool]

    :param enable_host_key: 是否开启主持人密钥，默认为false。 true：开启 false：关闭 修改周期性会议的主持人密钥适用于接下来的所有子会议。 
    :type enable_host_key: Optional[bool]

    :param enable_live: 是否开启直播,默认不开启 
    :type enable_live: Optional[bool]

    :param end_time: 会议结束时间戳（单位秒） 
    :type end_time: Optional[str]

    :param guests: 会议嘉宾列表，会议嘉宾不受会议密码和等候室的限制。不传该字段代表不修改。注意：传空数组会清空嘉宾列表。 
    :type guests: Optional[List[V1MeetingsPostRequestGuestsInner]]

    :param host_key: 主持人密钥，仅支持6位数字。 如开启主持人密钥后没有填写此项，将自动分配一个6位数字的密钥。 
    :type host_key: Optional[str]

    :param hosts: 主持人列表。 不传入该字段则不修改，传入空列表即覆盖为空。 
    :type hosts: Optional[List[V1MeetingsMeetingIdPutRequestHostsInner]]

    :param instanceid: 用户的终端设备类型： 0：PSTN 1：PC 2：Mac 3：Android 4：iOS 5：Web 6：iPad 7：Android Pad 8：小程序 9：voip、sip 设备 10：linux 20：Rooms for Touch Windows 21：Rooms for Touch MacOS 22：Rooms for Touch Android 30：Controller for Touch Windows 32：Controller for Touch Android 33：Controller for Touch iOS (required) 
    :type instanceid: int

    :param invitees: 邀请人列表，调用方用于标示用户的唯一 ID，仅支持邀请与会议创建者同企业的成员（企业内部请使用企业唯一用户标识；OAuth2.0 鉴权用户请使用 openId）。 企业唯一用户标识说明： 企业对接 SSO 时使用的员工唯一标识 ID。 企业调用创建用户接口时传递的 userid 参数。 注意：仅腾讯会议商业版和企业版可邀请参会者，邀请者列表仅支持300人；需要邀请超过300人的场景请调用 设置会议邀请成员 接口。 
    :type invitees: Optional[List[V1MeetingsPostRequestInviteesInner]]

    :param live_config:
    :type live_config: Optional[V1MeetingsMeetingIdPutRequestLiveConfig]

    :param location: 会议地点。最长支持18个汉字或36个英文字母。 
    :type location: Optional[str]

    :param media_set_type: 该参数仅提供给支持混合云的企业可见，默认值为0。 0：外部会议 1：内部会议 
    :type media_set_type: Optional[int]

    :param meeting_type: 默认值为0。  0：普通会议  1：周期性会议（周期性会议时 type 不能为快速会议，同一账号同时最多可预定50场周期性会议） 
    :type meeting_type: Optional[int]

    :param password: 会议密码（4~6位数字），可不填。如果将字段值改为空字符串\"\"，则表示取消会议密码 
    :type password: Optional[str]

    :param recurring_rule:
    :type recurring_rule: Optional[V1MeetingsMeetingIdPutRequestRecurringRule]

    :param settings:
    :type settings: Optional[V1MeetingsMeetingIdPutRequestSettings]

    :param start_time: 会议开始时间戳（单位秒） 
    :type start_time: Optional[str]

    :param subject: 会议主题 
    :type subject: Optional[str]

    :param time_zone: 时区，可参见 Oracle-TimeZone 标准。 
    :type time_zone: Optional[str]

    :param userid: 会议创建者 ID（企业内部请使用企业唯一用户标识；OAuth2.0 鉴权用户请使用 openId）。 企业唯一用户标识说明： 1. 企业对接 SSO 时使用的员工唯一标识 ID。 2. 企业调用创建用户接口时传递的 userid 参数。  (required) 
    :type userid: str
    """  # noqa: E501

    enable_doc_upload_permission: Optional[bool] = None
    enable_enroll: Optional[bool] = None
    enable_host_key: Optional[bool] = None
    enable_live: Optional[bool] = None
    end_time: Optional[str] = None
    guests: Optional[List[V1MeetingsPostRequestGuestsInner]] = None
    host_key: Optional[str] = None
    hosts: Optional[List[V1MeetingsMeetingIdPutRequestHostsInner]] = None
    instanceid: int
    invitees: Optional[List[V1MeetingsPostRequestInviteesInner]] = None
    live_config: Optional[V1MeetingsMeetingIdPutRequestLiveConfig] = None
    location: Optional[str] = None
    media_set_type: Optional[int] = None
    meeting_type: Optional[int] = None
    password: Optional[str] = None
    recurring_rule: Optional[V1MeetingsMeetingIdPutRequestRecurringRule] = None
    settings: Optional[V1MeetingsMeetingIdPutRequestSettings] = None
    start_time: Optional[str] = None
    subject: Optional[str] = None
    time_zone: Optional[str] = None
    userid: str
    additional_properties: Dict[str, Any] = {}

    def __init__(
        self,
        instanceid: int,
        userid: str,
        enable_doc_upload_permission: Optional[bool] = None,
        enable_enroll: Optional[bool] = None,
        enable_host_key: Optional[bool] = None,
        enable_live: Optional[bool] = None,
        end_time: Optional[str] = None,
        guests: Optional[List[V1MeetingsPostRequestGuestsInner] | List[Dict[str, Any]]] = None,
        host_key: Optional[str] = None,
        hosts: Optional[List[V1MeetingsMeetingIdPutRequestHostsInner] | List[Dict[str, Any]]] = None,
        invitees: Optional[List[V1MeetingsPostRequestInviteesInner] | List[Dict[str, Any]]] = None,
        live_config: Optional[V1MeetingsMeetingIdPutRequestLiveConfig | Dict[str, Any]] = None,
        location: Optional[str] = None,
        media_set_type: Optional[int] = None,
        meeting_type: Optional[int] = None,
        password: Optional[str] = None,
        recurring_rule: Optional[V1MeetingsMeetingIdPutRequestRecurringRule | Dict[str, Any]] = None,
        settings: Optional[V1MeetingsMeetingIdPutRequestSettings | Dict[str, Any]] = None,
        start_time: Optional[str] = None,
        subject: Optional[str] = None,
        time_zone: Optional[str] = None,
        **kwargs
    ):
        self.enable_doc_upload_permission = enable_doc_upload_permission
        self.enable_enroll = enable_enroll
        self.enable_host_key = enable_host_key
        self.enable_live = enable_live
        self.end_time = end_time
        
        if guests and isinstance(guests, (list, List)):
            self.guests = [V1MeetingsPostRequestGuestsInner(**_item) if isinstance(_item, (dict, Dict)) else _item for _item in guests]
        
        self.host_key = host_key
        
        if hosts and isinstance(hosts, (list, List)):
            self.hosts = [V1MeetingsMeetingIdPutRequestHostsInner(**_item) if isinstance(_item, (dict, Dict)) else _item for _item in hosts]
        
        self.instanceid = instanceid
        
        if invitees and isinstance(invitees, (list, List)):
            self.invitees = [V1MeetingsPostRequestInviteesInner(**_item) if isinstance(_item, (dict, Dict)) else _item for _item in invitees]
        
        self.live_config = V1MeetingsMeetingIdPutRequestLiveConfig(**live_config) if isinstance(live_config, (dict, Dict)) else live_config
        self.location = location
        self.media_set_type = media_set_type
        self.meeting_type = meeting_type
        self.password = password
        self.recurring_rule = V1MeetingsMeetingIdPutRequestRecurringRule(**recurring_rule) if isinstance(recurring_rule, (dict, Dict)) else recurring_rule
        self.settings = V1MeetingsMeetingIdPutRequestSettings(**settings) if isinstance(settings, (dict, Dict)) else settings
        self.start_time = start_time
        self.subject = subject
        self.time_zone = time_zone
        self.userid = userid

