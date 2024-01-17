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


class V1MeetingsPost200ResponseMeetingInfoListInnerSettings(object):
    """会议媒体参数配置

    :param allow_in_before_host: 是否允许成员在主持人进会前加入会议，默认值为 true。 true：允许 false：不允许 
    :type allow_in_before_host: Optional[bool]

    :param allow_screen_shared_watermark: 是否开启屏幕共享水印，默认值为 false。 true： 开启 false：不开启 
    :type allow_screen_shared_watermark: Optional[bool]

    :param allow_unmute_self: 允许参会者取消静音，默认值为 true。 true：开启 false：关闭 
    :type allow_unmute_self: Optional[bool]

    :param auto_in_waiting_room: 是否开启等候室，默认值为 false。 true：开启 false：不开启 
    :type auto_in_waiting_room: Optional[bool]

    :param auto_record_type: 自动会议录制类型。 none：禁用，表示不开启自动会议录制。 local：本地录制，表示主持人入会后自动开启本地录制。 cloud：云录制，表示主持人入会后自动开启云录制。 说明： 该参数依赖企业账户设置，当企业强制锁定后，该参数必须与企业配置保持一致。 仅客户端2.7及以上版本可生效。 
    :type auto_record_type: Optional[str]

    :param enable_host_pause_auto_record: 允许主持人暂停或者停止云录制，默认值为 true 开启，开启时，主持人允许暂停和停止云录制；当设置为关闭时，则主持人不允许暂停和关闭云录制。 说明： 该参数必须 auto_record_type 设置为“cloud”时才生效，该参数依赖企业账户设置，当企业强制锁定后，该参数必须与企业配置保持一致。 仅客户端2.7及以上版本生效。 
    :type enable_host_pause_auto_record: Optional[bool]

    :param mute_enable_join: 入会时静音，默认值为 true true：开启 false：关闭 
    :type mute_enable_join: Optional[bool]

    :param mute_enable_type_join: 成员入会时静音选项，默认值为2。 当同时传入“mute_enable_join”和“mute_enable_type_join”时，将以“mute_enable_type_join”的选项为准。 0：关闭 1：开启 2：超过6人后自动开启 
    :type mute_enable_type_join: Optional[int]

    :param only_enterprise_user_allowed: 是否仅企业内部成员可入会，默认值为 false。 true：仅企业内部用户可入会 false：所有人可入会 
    :type only_enterprise_user_allowed: Optional[bool]

    :param participant_join_auto_record: 当有参会成员入会时立即开启云录制，默认值为 false 关闭，关闭时，主持人入会自动开启云录制；当设置为开启时，则有参会成员入会自动开启云录制。 说明： 该参数必须 auto_record_type 设置为“cloud”时才生效，该参数依赖企业账户设置，当企业强制锁定后，该参数必须与企业配置保持一致。 仅客户端2.7及以上版本生效。 
    :type participant_join_auto_record: Optional[bool]

    :param play_ivr_on_join: 有新的与会者加入时播放提示音，暂不支持，可在客户端设置 
    :type play_ivr_on_join: Optional[bool]

    :param play_ivr_on_leave: 参会者离开时播放提示音，暂时不支持，可在客户端设置。 
    :type play_ivr_on_leave: Optional[bool]

    :param water_mark_type: 水印样式，默认为单排。当屏幕共享水印参数为开启时，此参数才生效。 0：单排 1：多排 
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
    only_enterprise_user_allowed: Optional[bool] = None
    participant_join_auto_record: Optional[bool] = None
    play_ivr_on_join: Optional[bool] = None
    play_ivr_on_leave: Optional[bool] = None
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
        only_enterprise_user_allowed: Optional[bool] = None,
        participant_join_auto_record: Optional[bool] = None,
        play_ivr_on_join: Optional[bool] = None,
        play_ivr_on_leave: Optional[bool] = None,
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
        self.only_enterprise_user_allowed = only_enterprise_user_allowed
        self.participant_join_auto_record = participant_join_auto_record
        self.play_ivr_on_join = play_ivr_on_join
        self.play_ivr_on_leave = play_ivr_on_leave
        self.water_mark_type = water_mark_type

