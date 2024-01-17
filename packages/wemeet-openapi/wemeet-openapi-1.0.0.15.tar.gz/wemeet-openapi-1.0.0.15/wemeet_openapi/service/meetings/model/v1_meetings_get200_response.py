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
from wemeet_openapi.service.meetings.model.v1_meetings_get200_response_meeting_info_list_inner import V1MeetingsGet200ResponseMeetingInfoListInner


class V1MeetingsGet200Response(object):
    """V1MeetingsGet200Response

    :param meeting_info_list:
    :type meeting_info_list: Optional[List[V1MeetingsGet200ResponseMeetingInfoListInner]]

    :param meeting_number: 会议数量。 
    :type meeting_number: Optional[int]

    :param next_cursory: 分页获取用户会议列表，查询的会议的最后一次修改时间值，UNIX 毫秒级时间戳，分页游标。 因目前一次查询返回会议数量最多为20，当用户会议较多时，如果会议总数量超过20，则需要再次查询。此参数为非必选参数，默认值为0，表示第一次查询利用会议开始时间北京时间当日零点进行查询。 查询返回输出参数“remaining”不为0时，表示还有会议需要继续查询。返回参数“next_cursory”的值即为下一次查询的 cursory 的值。 多次调用该查询接口直到输出参数“remaining”值为0。 当只使用 pos 作为分页条件时,可能会出现查询不到第二页,数据排序出现重复数据等情况与 pos 配合使用。 
    :type next_cursory: Optional[int]

    :param next_pos: 下次查询时请求里需要携带的 pos 参数。 
    :type next_pos: Optional[int]

    :param remaining: 是否还剩下会议；因目前一次查询返回会议数量最多为20，如果会议总数量超过20则此字段被置为非0，表示需要再次查询，且下次查询的“pos”参数需从本次响应的“next_pos”字段取值 
    :type remaining: Optional[int]
    """  # noqa: E501

    meeting_info_list: Optional[List[V1MeetingsGet200ResponseMeetingInfoListInner]] = None
    meeting_number: Optional[int] = None
    next_cursory: Optional[int] = None
    next_pos: Optional[int] = None
    remaining: Optional[int] = None
    additional_properties: Dict[str, Any] = {}

    def __init__(
        self,
        meeting_info_list: Optional[List[V1MeetingsGet200ResponseMeetingInfoListInner] | List[Dict[str, Any]]] = None,
        meeting_number: Optional[int] = None,
        next_cursory: Optional[int] = None,
        next_pos: Optional[int] = None,
        remaining: Optional[int] = None,
        **kwargs
    ):
        
        if meeting_info_list and isinstance(meeting_info_list, (list, List)):
            self.meeting_info_list = [V1MeetingsGet200ResponseMeetingInfoListInner(**_item) if isinstance(_item, (dict, Dict)) else _item for _item in meeting_info_list]
        
        self.meeting_number = meeting_number
        self.next_cursory = next_cursory
        self.next_pos = next_pos
        self.remaining = remaining

