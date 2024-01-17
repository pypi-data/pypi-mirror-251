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


class V1MeetingsGet200ResponseMeetingInfoListInnerSettings(object):
    """V1MeetingsGet200ResponseMeetingInfoListInnerSettings

    :param allow_in_before_host:
    :type allow_in_before_host: Optional[bool]

    :param allow_screen_shared_watermark:
    :type allow_screen_shared_watermark: Optional[bool]

    :param allow_unmute_self:
    :type allow_unmute_self: Optional[bool]

    :param auto_in_waiting_room:
    :type auto_in_waiting_room: Optional[bool]

    :param auto_record_type:
    :type auto_record_type: Optional[str]

    :param enable_host_pause_auto_record:
    :type enable_host_pause_auto_record: Optional[bool]

    :param mute_enable_join:
    :type mute_enable_join: Optional[bool]

    :param mute_enable_type_join:
    :type mute_enable_type_join: Optional[int]

    :param only_allow_enterprise_user_join:
    :type only_allow_enterprise_user_join: Optional[bool]

    :param participant_join_auto_record:
    :type participant_join_auto_record: Optional[bool]

    :param water_mark_type:
    :type water_mark_type: Optional[int]
    """  # noqa: E501

    allow_in_before_host: Optional[bool] = None
    allow_screen_shared_watermark: Optional[bool] = None
    allow_unmute_self: Optional[bool] = None
    auto_in_waiting_room: Optional[bool] = None
    auto_record_type: Optional[str] = None
    enable_host_pause_auto_record: Optional[bool] = None
    mute_enable_join: Optional[bool] = None
    mute_enable_type_join: Optional[int] = None
    only_allow_enterprise_user_join: Optional[bool] = None
    participant_join_auto_record: Optional[bool] = None
    water_mark_type: Optional[int] = None
    additional_properties: Dict[str, Any] = {}

    def __init__(
        self,
        allow_in_before_host: Optional[bool] = None,
        allow_screen_shared_watermark: Optional[bool] = None,
        allow_unmute_self: Optional[bool] = None,
        auto_in_waiting_room: Optional[bool] = None,
        auto_record_type: Optional[str] = None,
        enable_host_pause_auto_record: Optional[bool] = None,
        mute_enable_join: Optional[bool] = None,
        mute_enable_type_join: Optional[int] = None,
        only_allow_enterprise_user_join: Optional[bool] = None,
        participant_join_auto_record: Optional[bool] = None,
        water_mark_type: Optional[int] = None,
        **kwargs
    ):
        self.allow_in_before_host = allow_in_before_host
        self.allow_screen_shared_watermark = allow_screen_shared_watermark
        self.allow_unmute_self = allow_unmute_self
        self.auto_in_waiting_room = auto_in_waiting_room
        self.auto_record_type = auto_record_type
        self.enable_host_pause_auto_record = enable_host_pause_auto_record
        self.mute_enable_join = mute_enable_join
        self.mute_enable_type_join = mute_enable_type_join
        self.only_allow_enterprise_user_join = only_allow_enterprise_user_join
        self.participant_join_auto_record = participant_join_auto_record
        self.water_mark_type = water_mark_type

