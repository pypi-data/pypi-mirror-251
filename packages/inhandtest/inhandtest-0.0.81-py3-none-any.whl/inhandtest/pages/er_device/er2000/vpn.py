# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : pypi_common
@Time    : 2023/11/30 17:48
@Auth    : wangjw
@Email   : wangjiaw@inhand.com.cn
@File    : vpn.py
@IDE     : PyCharm
------------------------------------
"""
from inhandtest.pages.er_device.functions.functions import IpsecVpn, L2tpVpnServer, L2tpVpnClient, VxlanVpn


class L2tpVpn:
    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='ER2000', language='en', page=None, **kwargs):
        self.l2tp_vpn_server = L2tpVpnServer(host, username, password, protocol, port, model, language, page, **kwargs)
        self.l2tp_vpn_client = L2tpVpnClient(host, username, password, protocol, port, model, language, page, **kwargs)


class Vpn:
    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='ER2000', language='en', page=None, **kwargs):
        self.ipsec_vpn = IpsecVpn(host, username, password, protocol, port, model, language, page, **kwargs)
        self.l2tp_vpn = L2tpVpn(host, username, password, protocol, port, model, language, page, **kwargs)
        self.vxlan_vpn = VxlanVpn(host, username, password, protocol, port, model, language, page, **kwargs)
