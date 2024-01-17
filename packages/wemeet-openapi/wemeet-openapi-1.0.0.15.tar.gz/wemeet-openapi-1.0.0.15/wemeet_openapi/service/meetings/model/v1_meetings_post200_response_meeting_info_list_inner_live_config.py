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
from wemeet_openapi.service.meetings.model.v1_meetings_post_request_live_config_live_watermark import V1MeetingsPostRequestLiveConfigLiveWatermark


class V1MeetingsPost200ResponseMeetingInfoListInnerLiveConfig(object):
    """直播配置

    :param enable_live_im: 允许观众讨论，默认值为 false。 true：开启 false：不开启 
    :type enable_live_im: Optional[bool]

    :param enable_live_password: 是否开启直播密码，默认值false. true：开启, false：不开启 
    :type enable_live_password: Optional[bool]

    :param enable_live_replay: 开启直播回看，默认值为 false true：开启 false：不开启 
    :type enable_live_replay: Optional[bool]

    :param live_password: 直播密码。当设置开启直播密码时，该参数必填。 
    :type live_password: Optional[str]

    :param live_subject: 直播主题 
    :type live_subject: Optional[str]

    :param live_summary: 直播简介 
    :type live_summary: Optional[str]

    :param live_watermark:
    :type live_watermark: Optional[V1MeetingsPostRequestLiveConfigLiveWatermark]
    """  # noqa: E501

    enable_live_im: Optional[bool] = None
    enable_live_password: Optional[bool] = None
    enable_live_replay: Optional[bool] = None
    live_password: Optional[str] = None
    live_subject: Optional[str] = None
    live_summary: Optional[str] = None
    live_watermark: Optional[V1MeetingsPostRequestLiveConfigLiveWatermark] = None
    additional_properties: Dict[str, Any] = {}

    def __init__(
        self,
        enable_live_im: Optional[bool] = None,
        enable_live_password: Optional[bool] = None,
        enable_live_replay: Optional[bool] = None,
        live_password: Optional[str] = None,
        live_subject: Optional[str] = None,
        live_summary: Optional[str] = None,
        live_watermark: Optional[V1MeetingsPostRequestLiveConfigLiveWatermark | Dict[str, Any]] = None,
        **kwargs
    ):
        self.enable_live_im = enable_live_im
        self.enable_live_password = enable_live_password
        self.enable_live_replay = enable_live_replay
        self.live_password = live_password
        self.live_subject = live_subject
        self.live_summary = live_summary
        self.live_watermark = V1MeetingsPostRequestLiveConfigLiveWatermark(**live_watermark) if isinstance(live_watermark, (dict, Dict)) else live_watermark

