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
from wemeet_openapi.service.meetings.model.v1_meetings_post200_response_meeting_info_list_inner_hosts_inner import V1MeetingsPost200ResponseMeetingInfoListInnerHostsInner
from wemeet_openapi.service.meetings.model.v1_meetings_post200_response_meeting_info_list_inner_live_config import V1MeetingsPost200ResponseMeetingInfoListInnerLiveConfig
from wemeet_openapi.service.meetings.model.v1_meetings_post200_response_meeting_info_list_inner_hosts_inner import V1MeetingsPost200ResponseMeetingInfoListInnerHostsInner
from wemeet_openapi.service.meetings.model.v1_meetings_post200_response_meeting_info_list_inner_settings import V1MeetingsPost200ResponseMeetingInfoListInnerSettings


class V1MeetingsPost200ResponseMeetingInfoListInner(object):
    """V1MeetingsPost200ResponseMeetingInfoListInner

    :param enable_live: 是否开启直播。 
    :type enable_live: Optional[bool]

    :param end_time: 会议结束时间戳（单位秒） 
    :type end_time: Optional[str]

    :param host_key: 主持人密钥，仅支持6位数字。 如开启主持人密钥后没有填写此项，将自动分配一个6位数字的密钥。 
    :type host_key: Optional[str]

    :param hosts: 会议主持人的用户 ID，如果无指定，主持人将被设定为上文的 userid，即 API 调用者，仅商业版和企业版可指定主持人。 
    :type hosts: Optional[List[V1MeetingsPost200ResponseMeetingInfoListInnerHostsInner]]

    :param join_url: 加入会议 URL（单击链接直接加入会议）。 
    :type join_url: Optional[str]

    :param live_config:
    :type live_config: Optional[V1MeetingsPost200ResponseMeetingInfoListInnerLiveConfig]

    :param meeting_code: 会议 App 的呼入号码。 
    :type meeting_code: Optional[str]

    :param meeting_id: 会议ID  
    :type meeting_id: Optional[str]

    :param participants: 邀请的参会者用户 ID，仅商业版和企业版可邀请参会用户。 
    :type participants: Optional[List[V1MeetingsPost200ResponseMeetingInfoListInnerHostsInner]]

    :param password: 会议密码。 
    :type password: Optional[str]

    :param settings:
    :type settings: Optional[V1MeetingsPost200ResponseMeetingInfoListInnerSettings]

    :param start_time: 会议开始时间戳（单位秒），对于快速会议则为会议创建的时间。 
    :type start_time: Optional[str]

    :param subject: 会议主题 
    :type subject: Optional[str]

    :param user_non_registered: 邀请的参会者中未注册用户。 注意：仅腾讯会议商业版和企业版可获取该参数。 
    :type user_non_registered: Optional[List[str]]
    """  # noqa: E501

    enable_live: Optional[bool] = None
    end_time: Optional[str] = None
    host_key: Optional[str] = None
    hosts: Optional[List[V1MeetingsPost200ResponseMeetingInfoListInnerHostsInner]] = None
    join_url: Optional[str] = None
    live_config: Optional[V1MeetingsPost200ResponseMeetingInfoListInnerLiveConfig] = None
    meeting_code: Optional[str] = None
    meeting_id: Optional[str] = None
    participants: Optional[List[V1MeetingsPost200ResponseMeetingInfoListInnerHostsInner]] = None
    password: Optional[str] = None
    settings: Optional[V1MeetingsPost200ResponseMeetingInfoListInnerSettings] = None
    start_time: Optional[str] = None
    subject: Optional[str] = None
    user_non_registered: Optional[List[str]] = None
    additional_properties: Dict[str, Any] = {}

    def __init__(
        self,
        enable_live: Optional[bool] = None,
        end_time: Optional[str] = None,
        host_key: Optional[str] = None,
        hosts: Optional[List[V1MeetingsPost200ResponseMeetingInfoListInnerHostsInner] | List[Dict[str, Any]]] = None,
        join_url: Optional[str] = None,
        live_config: Optional[V1MeetingsPost200ResponseMeetingInfoListInnerLiveConfig | Dict[str, Any]] = None,
        meeting_code: Optional[str] = None,
        meeting_id: Optional[str] = None,
        participants: Optional[List[V1MeetingsPost200ResponseMeetingInfoListInnerHostsInner] | List[Dict[str, Any]]] = None,
        password: Optional[str] = None,
        settings: Optional[V1MeetingsPost200ResponseMeetingInfoListInnerSettings | Dict[str, Any]] = None,
        start_time: Optional[str] = None,
        subject: Optional[str] = None,
        user_non_registered: Optional[List[str]] = None,
        **kwargs
    ):
        self.enable_live = enable_live
        self.end_time = end_time
        self.host_key = host_key
        
        if hosts and isinstance(hosts, (list, List)):
            self.hosts = [V1MeetingsPost200ResponseMeetingInfoListInnerHostsInner(**_item) if isinstance(_item, (dict, Dict)) else _item for _item in hosts]
        
        self.join_url = join_url
        self.live_config = V1MeetingsPost200ResponseMeetingInfoListInnerLiveConfig(**live_config) if isinstance(live_config, (dict, Dict)) else live_config
        self.meeting_code = meeting_code
        self.meeting_id = meeting_id
        
        if participants and isinstance(participants, (list, List)):
            self.participants = [V1MeetingsPost200ResponseMeetingInfoListInnerHostsInner(**_item) if isinstance(_item, (dict, Dict)) else _item for _item in participants]
        
        self.password = password
        self.settings = V1MeetingsPost200ResponseMeetingInfoListInnerSettings(**settings) if isinstance(settings, (dict, Dict)) else settings
        self.start_time = start_time
        self.subject = subject
        
        if user_non_registered and isinstance(user_non_registered, (list, List)):
            self.user_non_registered = user_non_registered
        

