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


class V1MeetingsMeetingIdEnrollConfigPutRequestQuestionListInnerOptionListInner(object):
    """V1MeetingsMeetingIdEnrollConfigPutRequestQuestionListInnerOptionListInner

    :param content:
    :type content: Optional[str]
    """  # noqa: E501

    content: Optional[str] = None
    additional_properties: Dict[str, Any] = {}

    def __init__(
        self,
        content: Optional[str] = None,
        **kwargs
    ):
        self.content = content

