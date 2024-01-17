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


class V1MeetingsPostRequestRecurringRule(object):
    """周期性会议配置

    :param customized_recurring_days: 哪些天重复。根据 customized_recurring_type 和 customized_recurring_step 的不同，该字段可取值与表达含义不同。如需选择多个日期，加和即可。 customized_recurring_type = 0 时，传入该字段将被忽略。 详细请参见 自定义周期规则 API 调用示例 
    :type customized_recurring_days: Optional[int]

    :param customized_recurring_step: 每[n]（天、周、月）重复，使用自定义周期性会议时传入。 例如：customized_recurring_type=0 &amp;&amp; customized_recurring_step=5 表示每5天重复一次。 customized_recurring_type=2 &amp;&amp; customized_recurring_step=3 表示每3个月重复一次，重复的时间依赖于 customized_recurring_days 字段。 
    :type customized_recurring_step: Optional[int]

    :param customized_recurring_type: 自定义周期性会议的循环类型。 0：按天。 1：按周。 2：按月，以周为粒度重复。例如：每3个月的第二周的周四。 3：按月，以日期为粒度重复。例如：每3个月的16日。 按周；按月、以周为粒度； 按月、以日期为粒度时，需要包含会议开始时间所在的日期。 
    :type customized_recurring_type: Optional[int]

    :param recurring_type: 重复类型，默认值为0。 0：每天 1：每周一至周五 2：每周 3：每两周 4：每月 5：自定义，示例请参见 自定义周期规则 API 调用示例 
    :type recurring_type: Optional[int]

    :param until_count: 限定会议次数。 说明：每天、每个工作日、每周最大支持200场子会议；每两周、每月最大支持50场子会议。如未填写，则默认为7次。 
    :type until_count: Optional[int]

    :param until_date: 结束日期时间戳。 说明：结束日期与第一场会议的开始时间换算成的场次数不能超过以下限制：每天、每个工作日、每周最大支持200场子会议；每两周、每月最大支持50场子会议，例如：对于每天的重复类型，第一场会议开始时间为1609430400，则结束日期时间戳不能超过1609430400 + 200 × 24 × 60 × 60 - 1。如未填写，默认为当前日期往后推7天。 
    :type until_date: Optional[int]

    :param until_type: 结束重复类型，默认值为0。  0：按日期结束重复  1：按次数结束重复 
    :type until_type: Optional[int]
    """  # noqa: E501

    customized_recurring_days: Optional[int] = None
    customized_recurring_step: Optional[int] = None
    customized_recurring_type: Optional[int] = None
    recurring_type: Optional[int] = None
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
        until_count: Optional[int] = None,
        until_date: Optional[int] = None,
        until_type: Optional[int] = None,
        **kwargs
    ):
        self.customized_recurring_days = customized_recurring_days
        self.customized_recurring_step = customized_recurring_step
        self.customized_recurring_type = customized_recurring_type
        self.recurring_type = recurring_type
        self.until_count = until_count
        self.until_date = until_date
        self.until_type = until_type

