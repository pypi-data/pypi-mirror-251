# -*- coding: utf-8 -*-
# @Time    : 2023/5/15 15:33:43
# @Author  : Pane Li
# @File    : __init__.py.py
"""
__init__.py

"""
from inhandtest.pages.ingateway.ingateway import InGateway
from inhandtest.pages.er_device.eap600.eap600 import EAP600
from inhandtest.pages.er_device.er805.er805 import ER805
from inhandtest.pages.er_device.er2000.er2000 import ER2000

__all__ = [
    "InGateway",
    "EAP600",
    "ER805",
    "ER2000"
]
