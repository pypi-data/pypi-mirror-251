# coding: utf-8

"""
    腾讯会议OpenAPI

    SAAS版RESTFUL风格API

    API version: v1.0.0.18

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations

from typing import *

# import models into model package
from wemeet_openapi.service.meetings.model.v1_meetings_get200_response_meeting_info_list_inner_current_co_hosts_inner import V1MeetingsGet200ResponseMeetingInfoListInnerCurrentCoHostsInner
from wemeet_openapi.service.meetings.model.v1_meetings_get200_response_meeting_info_list_inner_current_hosts_inner import V1MeetingsGet200ResponseMeetingInfoListInnerCurrentHostsInner
from wemeet_openapi.service.meetings.model.v1_meetings_get200_response_meeting_info_list_inner_guests_inner import V1MeetingsGet200ResponseMeetingInfoListInnerGuestsInner
from wemeet_openapi.service.meetings.model.v1_meetings_get200_response_meeting_info_list_inner_current_co_hosts_inner import V1MeetingsGet200ResponseMeetingInfoListInnerCurrentCoHostsInner
from wemeet_openapi.service.meetings.model.v1_meetings_get200_response_meeting_info_list_inner_live_config import V1MeetingsGet200ResponseMeetingInfoListInnerLiveConfig
from wemeet_openapi.service.meetings.model.v1_meetings_get200_response_meeting_info_list_inner_current_co_hosts_inner import V1MeetingsGet200ResponseMeetingInfoListInnerCurrentCoHostsInner
from wemeet_openapi.service.meetings.model.v1_meetings_get200_response_meeting_info_list_inner_recurring_rule import V1MeetingsGet200ResponseMeetingInfoListInnerRecurringRule
from wemeet_openapi.service.meetings.model.v1_meetings_get200_response_meeting_info_list_inner_settings import V1MeetingsGet200ResponseMeetingInfoListInnerSettings
from wemeet_openapi.service.meetings.model.v1_meetings_get200_response_meeting_info_list_inner_sub_meetings_inner import V1MeetingsGet200ResponseMeetingInfoListInnerSubMeetingsInner


class V1MeetingsGet200ResponseMeetingInfoListInner(object):
    """V1MeetingsGet200ResponseMeetingInfoListInner

    :param current_co_hosts:
    :type current_co_hosts: Optional[List[V1MeetingsGet200ResponseMeetingInfoListInnerCurrentCoHostsInner]]

    :param current_hosts:
    :type current_hosts: Optional[List[V1MeetingsGet200ResponseMeetingInfoListInnerCurrentHostsInner]]

    :param current_sub_meeting_id: 当前子会议 ID（进行中 / 即将开始）。 
    :type current_sub_meeting_id: Optional[str]

    :param enable_doc_upload_permission:
    :type enable_doc_upload_permission: Optional[bool]

    :param enable_enroll:
    :type enable_enroll: Optional[bool]

    :param enable_host_key:
    :type enable_host_key: Optional[bool]

    :param enable_live:
    :type enable_live: Optional[bool]

    :param end_time:
    :type end_time: Optional[str]

    :param guests:
    :type guests: Optional[List[V1MeetingsGet200ResponseMeetingInfoListInnerGuestsInner]]

    :param has_more_sub_meeting: 0：无更多。  1：有更多子会议特例。 
    :type has_more_sub_meeting: Optional[int]

    :param has_vote:
    :type has_vote: Optional[bool]

    :param host_key:
    :type host_key: Optional[str]

    :param hosts:
    :type hosts: Optional[List[V1MeetingsGet200ResponseMeetingInfoListInnerCurrentCoHostsInner]]

    :param join_meeting_role: 查询者在会议中的角色： creator：创建者 hoster：主持人 invitee：被邀请者 
    :type join_meeting_role: Optional[str]

    :param join_url:
    :type join_url: Optional[str]

    :param live_config:
    :type live_config: Optional[V1MeetingsGet200ResponseMeetingInfoListInnerLiveConfig]

    :param location:
    :type location: Optional[str]

    :param media_set_type: 该参数仅提供给支持混合云的企业可见，默认值为0。 0：公网会议 1：专网会议 
    :type media_set_type: Optional[int]

    :param meeting_code:
    :type meeting_code: Optional[str]

    :param meeting_id:
    :type meeting_id: Optional[str]

    :param meeting_type:
    :type meeting_type: Optional[int]

    :param need_password:
    :type need_password: Optional[bool]

    :param participants:
    :type participants: Optional[List[V1MeetingsGet200ResponseMeetingInfoListInnerCurrentCoHostsInner]]

    :param password:
    :type password: Optional[str]

    :param recurring_rule:
    :type recurring_rule: Optional[V1MeetingsGet200ResponseMeetingInfoListInnerRecurringRule]

    :param remain_sub_meetings: 剩余子会议场数。 
    :type remain_sub_meetings: Optional[int]

    :param settings:
    :type settings: Optional[V1MeetingsGet200ResponseMeetingInfoListInnerSettings]

    :param start_time:
    :type start_time: Optional[str]

    :param status: 当前会议状态： MEETING_STATE_INVALID：非法或未知的会议状态，错误状态。 MEETING_STATE_INIT：待开始，会议预定到预定结束时间前，会议中无人。 MEETING_STATE_CANCELLED：已取消，主持人主动取消会议，待开始的会议才能取消，取消的会议无法再进入。 MEETING_STATE_STARTED：会议中，只要会议中有人即表示进行中。 MEETING_STATE_ENDED：已删除，结束时间后且会议中无人时，被主持人删除，已删除的会议无法再进入。 MEETING_STATE_NULL：无状态，过了预定结束时间，会议中无人。 MEETING_STATE_RECYCLED：已回收，过了预定开始时间30天，会议号被后台回收，无法再进入。      
    :type status: Optional[str]

    :param sub_meetings: 周期性子会议列表。 
    :type sub_meetings: Optional[List[V1MeetingsGet200ResponseMeetingInfoListInnerSubMeetingsInner]]

    :param subject:
    :type subject: Optional[str]

    :param sync_to_wework:
    :type sync_to_wework: Optional[bool]

    :param time_zone:
    :type time_zone: Optional[str]

    :param type: 会议类型： 0：预约会议类型 1：快速会议类型 
    :type type: Optional[int]
    """  # noqa: E501

    current_co_hosts: Optional[List[V1MeetingsGet200ResponseMeetingInfoListInnerCurrentCoHostsInner]] = None
    current_hosts: Optional[List[V1MeetingsGet200ResponseMeetingInfoListInnerCurrentHostsInner]] = None
    current_sub_meeting_id: Optional[str] = None
    enable_doc_upload_permission: Optional[bool] = None
    enable_enroll: Optional[bool] = None
    enable_host_key: Optional[bool] = None
    enable_live: Optional[bool] = None
    end_time: Optional[str] = None
    guests: Optional[List[V1MeetingsGet200ResponseMeetingInfoListInnerGuestsInner]] = None
    has_more_sub_meeting: Optional[int] = None
    has_vote: Optional[bool] = None
    host_key: Optional[str] = None
    hosts: Optional[List[V1MeetingsGet200ResponseMeetingInfoListInnerCurrentCoHostsInner]] = None
    join_meeting_role: Optional[str] = None
    join_url: Optional[str] = None
    live_config: Optional[V1MeetingsGet200ResponseMeetingInfoListInnerLiveConfig] = None
    location: Optional[str] = None
    media_set_type: Optional[int] = None
    meeting_code: Optional[str] = None
    meeting_id: Optional[str] = None
    meeting_type: Optional[int] = None
    need_password: Optional[bool] = None
    participants: Optional[List[V1MeetingsGet200ResponseMeetingInfoListInnerCurrentCoHostsInner]] = None
    password: Optional[str] = None
    recurring_rule: Optional[V1MeetingsGet200ResponseMeetingInfoListInnerRecurringRule] = None
    remain_sub_meetings: Optional[int] = None
    settings: Optional[V1MeetingsGet200ResponseMeetingInfoListInnerSettings] = None
    start_time: Optional[str] = None
    status: Optional[str] = None
    sub_meetings: Optional[List[V1MeetingsGet200ResponseMeetingInfoListInnerSubMeetingsInner]] = None
    subject: Optional[str] = None
    sync_to_wework: Optional[bool] = None
    time_zone: Optional[str] = None
    type: Optional[int] = None
    additional_properties: Dict[str, Any] = {}

    def __init__(
        self,
        current_co_hosts: Optional[List[V1MeetingsGet200ResponseMeetingInfoListInnerCurrentCoHostsInner] | List[Dict[str, Any]]] = None,
        current_hosts: Optional[List[V1MeetingsGet200ResponseMeetingInfoListInnerCurrentHostsInner] | List[Dict[str, Any]]] = None,
        current_sub_meeting_id: Optional[str] = None,
        enable_doc_upload_permission: Optional[bool] = None,
        enable_enroll: Optional[bool] = None,
        enable_host_key: Optional[bool] = None,
        enable_live: Optional[bool] = None,
        end_time: Optional[str] = None,
        guests: Optional[List[V1MeetingsGet200ResponseMeetingInfoListInnerGuestsInner] | List[Dict[str, Any]]] = None,
        has_more_sub_meeting: Optional[int] = None,
        has_vote: Optional[bool] = None,
        host_key: Optional[str] = None,
        hosts: Optional[List[V1MeetingsGet200ResponseMeetingInfoListInnerCurrentCoHostsInner] | List[Dict[str, Any]]] = None,
        join_meeting_role: Optional[str] = None,
        join_url: Optional[str] = None,
        live_config: Optional[V1MeetingsGet200ResponseMeetingInfoListInnerLiveConfig | Dict[str, Any]] = None,
        location: Optional[str] = None,
        media_set_type: Optional[int] = None,
        meeting_code: Optional[str] = None,
        meeting_id: Optional[str] = None,
        meeting_type: Optional[int] = None,
        need_password: Optional[bool] = None,
        participants: Optional[List[V1MeetingsGet200ResponseMeetingInfoListInnerCurrentCoHostsInner] | List[Dict[str, Any]]] = None,
        password: Optional[str] = None,
        recurring_rule: Optional[V1MeetingsGet200ResponseMeetingInfoListInnerRecurringRule | Dict[str, Any]] = None,
        remain_sub_meetings: Optional[int] = None,
        settings: Optional[V1MeetingsGet200ResponseMeetingInfoListInnerSettings | Dict[str, Any]] = None,
        start_time: Optional[str] = None,
        status: Optional[str] = None,
        sub_meetings: Optional[List[V1MeetingsGet200ResponseMeetingInfoListInnerSubMeetingsInner] | List[Dict[str, Any]]] = None,
        subject: Optional[str] = None,
        sync_to_wework: Optional[bool] = None,
        time_zone: Optional[str] = None,
        type: Optional[int] = None,
        **kwargs
    ):
        
        if current_co_hosts and isinstance(current_co_hosts, (list, List)):
            self.current_co_hosts = [V1MeetingsGet200ResponseMeetingInfoListInnerCurrentCoHostsInner(**_item) if isinstance(_item, (dict, Dict)) else _item for _item in current_co_hosts]
        
        
        if current_hosts and isinstance(current_hosts, (list, List)):
            self.current_hosts = [V1MeetingsGet200ResponseMeetingInfoListInnerCurrentHostsInner(**_item) if isinstance(_item, (dict, Dict)) else _item for _item in current_hosts]
        
        self.current_sub_meeting_id = current_sub_meeting_id
        self.enable_doc_upload_permission = enable_doc_upload_permission
        self.enable_enroll = enable_enroll
        self.enable_host_key = enable_host_key
        self.enable_live = enable_live
        self.end_time = end_time
        
        if guests and isinstance(guests, (list, List)):
            self.guests = [V1MeetingsGet200ResponseMeetingInfoListInnerGuestsInner(**_item) if isinstance(_item, (dict, Dict)) else _item for _item in guests]
        
        self.has_more_sub_meeting = has_more_sub_meeting
        self.has_vote = has_vote
        self.host_key = host_key
        
        if hosts and isinstance(hosts, (list, List)):
            self.hosts = [V1MeetingsGet200ResponseMeetingInfoListInnerCurrentCoHostsInner(**_item) if isinstance(_item, (dict, Dict)) else _item for _item in hosts]
        
        self.join_meeting_role = join_meeting_role
        self.join_url = join_url
        self.live_config = V1MeetingsGet200ResponseMeetingInfoListInnerLiveConfig(**live_config) if isinstance(live_config, (dict, Dict)) else live_config
        self.location = location
        self.media_set_type = media_set_type
        self.meeting_code = meeting_code
        self.meeting_id = meeting_id
        self.meeting_type = meeting_type
        self.need_password = need_password
        
        if participants and isinstance(participants, (list, List)):
            self.participants = [V1MeetingsGet200ResponseMeetingInfoListInnerCurrentCoHostsInner(**_item) if isinstance(_item, (dict, Dict)) else _item for _item in participants]
        
        self.password = password
        self.recurring_rule = V1MeetingsGet200ResponseMeetingInfoListInnerRecurringRule(**recurring_rule) if isinstance(recurring_rule, (dict, Dict)) else recurring_rule
        self.remain_sub_meetings = remain_sub_meetings
        self.settings = V1MeetingsGet200ResponseMeetingInfoListInnerSettings(**settings) if isinstance(settings, (dict, Dict)) else settings
        self.start_time = start_time
        self.status = status
        
        if sub_meetings and isinstance(sub_meetings, (list, List)):
            self.sub_meetings = [V1MeetingsGet200ResponseMeetingInfoListInnerSubMeetingsInner(**_item) if isinstance(_item, (dict, Dict)) else _item for _item in sub_meetings]
        
        self.subject = subject
        self.sync_to_wework = sync_to_wework
        self.time_zone = time_zone
        self.type = type

