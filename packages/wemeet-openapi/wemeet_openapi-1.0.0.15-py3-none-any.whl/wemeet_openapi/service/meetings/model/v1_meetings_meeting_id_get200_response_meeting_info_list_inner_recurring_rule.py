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


class V1MeetingsMeetingIdGet200ResponseMeetingInfoListInnerRecurringRule(object):
    """V1MeetingsMeetingIdGet200ResponseMeetingInfoListInnerRecurringRule

    :param customized_recurring_days:
    :type customized_recurring_days: Optional[int]

    :param customized_recurring_step:
    :type customized_recurring_step: Optional[int]

    :param customized_recurring_type:
    :type customized_recurring_type: Optional[int]

    :param recurring_type:
    :type recurring_type: Optional[int]

    :param until_count:
    :type until_count: Optional[int]

    :param until_date:
    :type until_date: Optional[int]

    :param until_type:
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

