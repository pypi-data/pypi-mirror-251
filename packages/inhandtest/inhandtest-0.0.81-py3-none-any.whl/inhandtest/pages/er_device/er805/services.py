# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : pypi_common
@Time    : 2023/12/20 14:19
@Auth    : wangjw
@Email   : wangjiaw@inhand.com.cn
@File    : services.py
@IDE     : PyCharm
------------------------------------
"""
from inhandtest.pages.er_device.functions.functions import InterfaceManagement, DhcpServer, DnsServer, FixedAddressList, \
    StaticRoutes, DynamicDns, PassthroughSettings


class Services:
    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='ER805', language='en', page=None, **kwargs):
        self.interface_management = InterfaceManagement(host, username, password, protocol, port, model, language, page,
                                                        **kwargs)
        self.dhcp_server = DhcpServer(host, username, password, protocol, port, model, language, page, **kwargs)
        self.dns_server = DnsServer(host, username, password, protocol, port, model, language, page, **kwargs)
        self.fixed_address_list = FixedAddressList(host, username, password, protocol, port, model, language, page,
                                                   **kwargs)
        self.static_routes = StaticRoutes(host, username, password, protocol, port, model, language, page, **kwargs)
        self.dynamic_dns = DynamicDns(host, username, password, protocol, port, model, language, page, **kwargs)
        self.passthrough_settings = PassthroughSettings(host, username, password, protocol, port, model, language, page,
                                                        **kwargs)