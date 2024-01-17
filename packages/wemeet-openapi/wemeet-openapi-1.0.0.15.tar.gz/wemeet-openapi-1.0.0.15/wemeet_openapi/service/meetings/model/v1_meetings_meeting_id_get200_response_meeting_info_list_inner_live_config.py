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
from wemeet_openapi.service.meetings.model.v1_meetings_get200_response_meeting_info_list_inner_live_config_live_watermark import V1MeetingsGet200ResponseMeetingInfoListInnerLiveConfigLiveWatermark


class V1MeetingsMeetingIdGet200ResponseMeetingInfoListInnerLiveConfig(object):
    """V1MeetingsMeetingIdGet200ResponseMeetingInfoListInnerLiveConfig

    :param enable_live_im:
    :type enable_live_im: Optional[bool]

    :param enable_live_replay:
    :type enable_live_replay: Optional[bool]

    :param live_addr:
    :type live_addr: Optional[str]

    :param live_password:
    :type live_password: Optional[str]

    :param live_subject:
    :type live_subject: Optional[str]

    :param live_summary:
    :type live_summary: Optional[str]

    :param live_watermark:
    :type live_watermark: Optional[V1MeetingsGet200ResponseMeetingInfoListInnerLiveConfigLiveWatermark]
    """  # noqa: E501

    enable_live_im: Optional[bool] = None
    enable_live_replay: Optional[bool] = None
    live_addr: Optional[str] = None
    live_password: Optional[str] = None
    live_subject: Optional[str] = None
    live_summary: Optional[str] = None
    live_watermark: Optional[V1MeetingsGet200ResponseMeetingInfoListInnerLiveConfigLiveWatermark] = None
    additional_properties: Dict[str, Any] = {}

    def __init__(
        self,
        enable_live_im: Optional[bool] = None,
        enable_live_replay: Optional[bool] = None,
        live_addr: Optional[str] = None,
        live_password: Optional[str] = None,
        live_subject: Optional[str] = None,
        live_summary: Optional[str] = None,
        live_watermark: Optional[V1MeetingsGet200ResponseMeetingInfoListInnerLiveConfigLiveWatermark | Dict[str, Any]] = None,
        **kwargs
    ):
        self.enable_live_im = enable_live_im
        self.enable_live_replay = enable_live_replay
        self.live_addr = live_addr
        self.live_password = live_password
        self.live_subject = live_subject
        self.live_summary = live_summary
        self.live_watermark = V1MeetingsGet200ResponseMeetingInfoListInnerLiveConfigLiveWatermark(**live_watermark) if isinstance(live_watermark, (dict, Dict)) else live_watermark

