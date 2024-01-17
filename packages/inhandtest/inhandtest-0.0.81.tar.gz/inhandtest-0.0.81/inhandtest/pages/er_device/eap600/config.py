# -*- coding: utf-8 -*-
# @Time    : 2023/11/30 16:35:37
# @Author  : Pane Li
# @File    : config.py
"""
config

"""
from inhandtest.pages.er_device.functions.functions import LanOrLocalNetwork


class Config:
    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='EAP600', language='en', page=None, **kwargs):
        self.lan = LanOrLocalNetwork(host, username, password, protocol, port, model, language, page, **kwargs)
