# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2024-01-11 22:00:14
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Baidu API chat methods.
"""


from typing import Any, List, Dict, Literal, Optional
from reytool.ros import RFile
from reytool.rtime import wait

from .rbaidu_base import RAPIBaidu


class RAPIBaiduChat(RAPIBaidu):
    """
    Rey's `Baidu API chat` type.
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
        super().__init__(key, secret)
        self.chat_records: Dict[str, List[Dict[Literal["time", "user", "text"], Any]]] = {}


    def chat(
        self,
        text: str,
        path: Optional[str] = None
    ) -> bytes:
        """
        Generate voice file from text.

        Parameters
        ----------
        text : Text, length cannot exceed 60.
        path : File save path.
            - `None` : Not save.

        Returns
        -------
        Voice bytes data.
        """

        # Get parameter.
        url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro"
        params = {"access_token": self.token}
        headers = {"Content-Type": "application/json"}
        data = {
            "messages": ""
        }

        # Request.
        response = self.request(
            url,
            data=data,
            headers=headers
        )

        # Record.
        self.record(
            text=text,
            path=path
        )

        # Extract.
        file_bytes = response.content

        # Save.
        if path is not None:
            rfile = RFile(path)
            rfile.write(file_bytes)

        return file_bytes