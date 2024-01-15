# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2024-01-11 21:56:56
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Baidu API base methods.
"""


from typing import Any, List, Dict, Literal
from requests import Response
from uuid import uuid1
from reytool.rcomm import request as reytool_request
from reytool.rtime import now


class RAPIBaidu(object):
    """
    Rey's `Baidu API` type.
    """


    def __init__(
        self,
        key: str,
        secret: str
    ) -> None:
        """
        Build `Baidu API` instance.

        Parameters
        ----------
        key : API key.
        secret : API secret.
        """

        # Set attribute.
        self.key = key
        self.secret = secret
        self.token = self.get_token()
        self.cuid = uuid1()
        self.call_records: List[Dict[Literal["time", "data"], Any]] = []


    def request(
        self,
        *args: Any,
        **kwargs: Any
    ) -> Response:
        """
        Request.

        Parameters
        ----------
        args : Position arguments of function.
        kwargs : Keyword arguments of function.

        Returns
        -------
        `Response` instance.
        """

        # Request.
        response = reytool_request(*args, **kwargs)

        # Check.
        content_type = response.headers["Content-Type"]
        if content_type[:16] == "application/json":
            response_json: Dict = response.json()
            if "error_code" in response_json:
                raise AssertionError("Baidu API text to image task failed", response_json)

        return response


    def get_token(self) -> str:
        """
        Get token.

        Returns
        -------
        Token.
        """

        # Get parameter.
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {
            "grant_type": "client_credentials",
            "client_id": self.key,
            "client_secret": self.secret
        }

        # Request.
        response = self.request(
            url,
            params,
            method="post"
        )

        # Extract.
        response_json = response.json()
        token = response_json["access_token"]

        return token


    def record(
        self,
        **data: Any
    ) -> None:
        """
        Record usage.

        Parameters
        ----------
        data : Record data.
        """

        # Get parameter.
        record = {
            "time": now(),
            "data": data
        }

        # Record.
        self.call_records.append(record)