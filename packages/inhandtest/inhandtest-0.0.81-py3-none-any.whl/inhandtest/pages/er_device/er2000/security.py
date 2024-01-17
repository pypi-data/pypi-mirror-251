# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : pypi_common
@Time    : 2023/11/2 16:15
@Auth    : wangjw
@Email   : wangjiaw@inhand.com.cn
@File    : security.py
@IDE     : PyCharm
------------------------------------
"""
from inhandtest.pages.er_device.functions.functions import InboundRules, outboundRules, PortForwarding, Nat, \
    MacAddressFilter, DominNameFilter, PolicyBasedRouting, TrafficShaping


class Firewall:
    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='ER2000', language='en', page=None, **kwargs):
        self.inbound_rules = InboundRules(host, username, password, protocol, port, model, language, page, **kwargs)
        self.outbound_rules = outboundRules(host, username, password, protocol, port, model, language, page, **kwargs)
        self.port_forwarding = PortForwarding(host, username, password, protocol, port, model, language, page, **kwargs)
        self.nat = Nat(host, username, password, protocol, port, model, language, page, **kwargs)
        self.mac_address_filter = MacAddressFilter(host, username, password, protocol, port, model, language, page,
                                                   **kwargs)
        self.domin_name_filter = DominNameFilter(host, username, password, protocol, port, model, language, page,
                                                 **kwargs)


class Security:
    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='ER2000', language='en', page=None, **kwargs):
        self.firewall = Firewall(host, username, password, protocol, port, model, language, page, **kwargs)
        self.policy_based_routing = PolicyBasedRouting(host, username, password, protocol, port, model, language, page,
                                                       **kwargs)
        self.traffic_shaping = TrafficShaping(host, username, password, protocol, port, model, language, page,
                                              **kwargs)
