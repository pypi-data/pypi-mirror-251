# -*- coding: utf-8 -*-
# @Time    : 2023/12/26 13:28
# @Author  : tc
# @File    : wifi.py
from inhandtest.pages.er_device.functions.functions import Ssids, Portal


class Wifi:
    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='ER805', language='en', page=None, **kwargs):
        self.ssids = Ssids(host, username, password, protocol, port, model, language, page, **kwargs)
        self.portal = Portal(host, username, password, protocol, port, model, language, page, **kwargs)
