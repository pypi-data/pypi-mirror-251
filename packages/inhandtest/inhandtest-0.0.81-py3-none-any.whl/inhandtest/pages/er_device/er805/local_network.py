# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : pypi_common
@Time    : 2023/11/28 10:43
@Auth    : wangjw
@Email   : wangjiaw@inhand.com.cn
@File    : local_network.py
@IDE     : PyCharm
------------------------------------
"""
from inhandtest.pages.er_device.functions.functions import LanOrLocalNetwork


class LocalNetwork:
    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='ER805', language='en', page=None, **kwargs):
        self.localnetwork = LanOrLocalNetwork(host, username, password, protocol, port, model, language, page, **kwargs)
