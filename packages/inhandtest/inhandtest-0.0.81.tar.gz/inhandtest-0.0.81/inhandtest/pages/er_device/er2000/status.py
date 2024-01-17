# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : pypi_common
@Time    : 2023/12/25 16:36
@Auth    : wangjw
@Email   : wangjiaw@inhand.com.cn
@File    : status.py
@IDE     : PyCharm
------------------------------------
"""
from inhandtest.pages.er_device.functions.functions import Clients, IpsecStatus, L2tpStatus, LinkMonitoring, \
    PassthroughStatus, CellularSignal, Events, Logs


class Vpn:
    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='ER2000', language='en', page=None, **kwargs):
        self.ipsec = IpsecStatus(host, username, password, protocol, port, model, language, page, **kwargs)
        self.l2tp = L2tpStatus(host, username, password, protocol, port, model, language, page, **kwargs)


class Status:
    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='ER2000', language='en', page=None, **kwargs):
        self.clients = Clients(host, username, password, protocol, port, model, language, page, **kwargs)
        self.vpn = Vpn(host, username, password, protocol, port, model, language, page, **kwargs)
        self.link_monitoring = LinkMonitoring(host, username, password, protocol, port, model, language, page, **kwargs)
        self.passthrough = PassthroughStatus(host, username, password, protocol, port, model, language, page, **kwargs)
        self.cellular_signal = CellularSignal(host, username, password, protocol, port, model, language, page, **kwargs)
        self.events = Events(host, username, password, protocol, port, model, language, page, **kwargs)
        self.logs = Logs(host, username, password, protocol, port, model, language, page, **kwargs)
