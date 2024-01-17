# -*- coding: utf-8 -*-
# @Time    : 2023/12/19 13:55
# @Author  : tc
# @File    : system.py

from inhandtest.pages.er_device.functions.functions import CloudManagement, RemoteAccessControl, SystemClock, \
    DeviceOptions, ConfigurationManagement, DeviceAlarms, Tools, ScheduledReboot, LogServer, AccountManagement, \
    OtherSettings


class System:
    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='ER805', language='en', page=None, **kwargs):
        self.cloud_management = CloudManagement(host, username, password, protocol, port, model, language, page,
                                                **kwargs)
        self.remote_access_control = RemoteAccessControl(host, username, password, protocol, port, model, language,
                                                         page, **kwargs)
        self.system_clock = SystemClock(host, username, password, protocol, port, model, language, page, **kwargs)
        self.device_options = DeviceOptions(host, username, password, protocol, port, model, language, page, **kwargs)
        self.configuration_management = ConfigurationManagement(host, username, password, protocol, port, model,
                                                                language, page, **kwargs)
        self.device_alarms = DeviceAlarms(host, username, password, protocol, port, model, language, page, **kwargs)
        self.tools = Tools(host, username, password, protocol, port, model, language, page, **kwargs)
        self.schedule_reboot = ScheduledReboot(host, username, password, protocol, port, model, language, page,
                                               **kwargs)
        self.log_server = LogServer(host, username, password, protocol, port, model, language, page, **kwargs)
        self.account_management = AccountManagement(host, username, password, protocol, port, model, language, page,
                                                    **kwargs)
        self.other_settings = OtherSettings(host, username, password, protocol, port, model, language, page, **kwargs)
