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


class V1MeetingsPostRequestLiveConfigLiveWatermark(object):
    """直播水印对象

    :param watermark_opt: 水印选项，默认为0。 0：默认水印 1：无水印 
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

