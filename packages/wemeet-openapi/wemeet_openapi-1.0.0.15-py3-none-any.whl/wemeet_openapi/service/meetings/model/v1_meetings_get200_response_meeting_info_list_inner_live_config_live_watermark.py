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


class V1MeetingsGet200ResponseMeetingInfoListInnerLiveConfigLiveWatermark(object):
    """V1MeetingsGet200ResponseMeetingInfoListInnerLiveConfigLiveWatermark

    :param watermark_opt:
    :type watermark_opt: Optional[int]
    """  # noqa: E501

    watermark_opt: Optional[int] = None
    additional_properties: Dict[str, Any] = {}

    def __init__(
        self,
        watermark_opt: Optional[int] = None,
        **kwargs
    ):
        self.watermark_opt = watermark_opt

