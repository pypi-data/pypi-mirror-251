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
from wemeet_openapi.service.meetings.model.v1_meetings_meeting_id_put200_response_meeting_info_list_inner_live_config import V1MeetingsMeetingIdPut200ResponseMeetingInfoListInnerLiveConfig


class V1MeetingsMeetingIdPut200ResponseMeetingInfoListInner(object):
    """V1MeetingsMeetingIdPut200ResponseMeetingInfoListInner

    :param enable_live: 是否开启直播 
    :type enable_live: Optional[bool]

    :param host_key: 主持人密钥，仅支持6位数字。 如开启主持人密钥后没有填写此项，将自动分配一个6位数字的密钥。  
    :type host_key: Optional[str]

    :param live_config:
    :type live_config: Optional[V1MeetingsMeetingIdPut200ResponseMeetingInfoListInnerLiveConfig]

    :param meeting_code: 会议号码 
    :type meeting_code: Optional[str]

    :param meeting_id: 会议的唯一 ID 
    :type meeting_id: Optional[str]
    """  # noqa: E501

    enable_live: Optional[bool] = None
    host_key: Optional[str] = None
    live_config: Optional[V1MeetingsMeetingIdPut200ResponseMeetingInfoListInnerLiveConfig] = None
    meeting_code: Optional[str] = None
    meeting_id: Optional[str] = None
    additional_properties: Dict[str, Any] = {}

    def __init__(
        self,
        enable_live: Optional[bool] = None,
        host_key: Optional[str] = None,
        live_config: Optional[V1MeetingsMeetingIdPut200ResponseMeetingInfoListInnerLiveConfig | Dict[str, Any]] = None,
        meeting_code: Optional[str] = None,
        meeting_id: Optional[str] = None,
        **kwargs
    ):
        self.enable_live = enable_live
        self.host_key = host_key
        self.live_config = V1MeetingsMeetingIdPut200ResponseMeetingInfoListInnerLiveConfig(**live_config) if isinstance(live_config, (dict, Dict)) else live_config
        self.meeting_code = meeting_code
        self.meeting_id = meeting_id

