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


class V1MeetingsMeetingIdPutRequestRecurringRule(object):
    """周期性会议配置，meeting_type 为1时必填。

    :param customized_recurring_days: 哪些天重复。根据 customized_recurring_type 和 customized_recurring_step 的不同，该字段可取值与表达含义不同。如需选择多个日期，加和即可。 customized_recurring_type = 0 时，传入该字段将被忽略。 详细请参见 自定义周期规则 API 调用示例 
    :type customized_recurring_days: Optional[int]

    :param customized_recurring_step: 每[n]（天、周、月）重复，使用自定义周期性会议时传入。 例如：customized_recurring_type=0 && customized_recurring_step=5 表示每5天重复一次。 customized_recurring_type=2 && customized_recurring_step=3 表示每3个月重复一次，重复的时间依赖于 customized_recurring_days 字段。 
    :type customized_recurring_step: Optional[int]

    :param customized_recurring_type: 自定义周期性会议的循环类型。 0：按天。 1：按周。 2：按月，以周为粒度重复。例如：每3个月的第二周的周四。 3：按月，以日期为粒度重复。例如：每3个月的16日。 按周；按月、以周为粒度； 按月、以日期为粒度时，需要包含会议开始时间所在的日期。 
    :type customized_recurring_type: Optional[int]

    :param recurring_type: 重复类型，默认值为0。 0：每天 1：每周一至周五 2：每周 3：每两周 4：每月 5：自定义，示例请参见 自定义周期规则 API 调用示例 
    :type recurring_type: Optional[int]

    :param sub_meeting_id: 子会议 ID，表示修改该子会议时间，不可与周期性会议规则同时修改。 如不填写，默认修改整个周期性会议时间。 
    :type sub_meeting_id: Optional[str]

    :param until_count: 限定会议次数（1-50次）。 
    :type until_count: Optional[int]

    :param until_date: 结束日期时间戳，最大支持预定50场子会议。 
    :type until_date: Optional[int]

    :param until_type: 结束重复类型。 0：按日期结束重复 1：按次数结束重复 
    :type until_type: Optional[int]
    """  # noqa: E501

    customized_recurring_days: Optional[int] = None
    customized_recurring_step: Optional[int] = None
    customized_recurring_type: Optional[int] = None
    recurring_type: Optional[int] = None
    sub_meeting_id: Optional[str] = None
    until_count: Optional[int] = None
    until_date: Optional[int] = None
    until_type: Optional[int] = None
    additional_properties: Dict[str, Any] = {}

    def __init__(
        self,
        customized_recurring_days: Optional[int] = None,
        customized_recurring_step: Optional[int] = None,
        customized_recurring_type: Optional[int] = None,
        recurring_type: Optional[int] = None,
        sub_meeting_id: Optional[str] = None,
        until_count: Optional[int] = None,
        until_date: Optional[int] = None,
        until_type: Optional[int] = None,
        **kwargs
    ):
        self.customized_recurring_days = customized_recurring_days
        self.customized_recurring_step = customized_recurring_step
        self.customized_recurring_type = customized_recurring_type
        self.recurring_type = recurring_type
        self.sub_meeting_id = sub_meeting_id
        self.until_count = until_count
        self.until_date = until_date
        self.until_type = until_type

