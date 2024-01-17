# -*- coding: utf-8 -*-
# @Time    : 2023/11/30 16:18:00
# @Author  : Pane Li
# @File    : functions.py
"""
functions

"""
import os
import time
from datetime import datetime
import allure
from inhandtest.base_page import BasePage
from inhandtest.file import read_yaml_file
from inhandtest.mail import delete_all_mail, receive_last_mail
from inhandtest.pages.er_device.functions.functions_locators import FunctionsLocators
from inhandtest.tools import loop_inspector


class LinkMonitoring(BasePage):
    @allure.step('断言链路健康状态')
    @loop_inspector('link_health_status')
    def assert_status(self, uplink: str, **kwargs):
        """
        :param uplink: 'WAN1'|'WAN2'|'Cellular'|'Wi-Fi(STA)'
        :param kwargs:
            status: str, '"up" in "${value}"'|'"down" in "${value}"'|'"abnormal" in "${value}"'|'"disable" in "${value}"'
            carrier: str, 可以是'${value}'=='str' 等表达式
            usage_up: int, 可以是'${value}'=='str' 等表达式
            usage_up_unit: str, 可以是'${value}'=='str' 等表达式
            usage_down: str, 可以是'${value}'=='str' 等表达式
            usage_down_unit: str, 可以是'${value}'=='str' 等表达式
            throughput_up: str, 可以是'${value}'=='str' 等表达式
            throughput_up_unit: str, 可以是'${value}'=='str' 等表达式
            throughput_down: str, 可以是'${value}'=='str' 等表达式
            throughput_down_unit: str, 可以是'${value}'=='str' 等表达式
            latency: str, 可以是'${value}'=='str' 等表达式
            latency_unit: str, 可以是'${value}'=='str' 等表达式
            loss: str, 可以是'${value}'=='str' 等表达式
            signal_strength: str, 可以是'${value}'=='str' 等表达式
            exist: '"${value}"=="None"'时校验不存在, 默认校验存在
        :return:
        """
        if kwargs:
            self.access_menu('status.link_monitoring')
            locators = FunctionsLocators(self.page, self.locale, self.model).link_health_status(uplink)
            return self.eval_locator_attribute(kwargs, locators)

    @allure.step('获取链路健康状态')
    def get_status(self, name: str, keys: str or list or tuple) -> str or dict or None:
        """

        :param name: str or list or tuple 一个或多个链路名称
        :param keys: str or list or tuple , value
        :return: value or {'name1': value}
        """

        if name:
            link_health_locators = FunctionsLocators(self.page, self.locale, self.model).link_health_status(name)
            self.access_menu('status.link_monitoring')
            return self.get_text(keys, link_health_locators)

    @allure.step('校验链路健康曲线图及数据')
    def assert_link_quality_history(self, interface, assert_interface=True):
        """
        :param interface: 需要校验的接口 'WAN1'|'WAN2'|'Cellular'|'Wi-Fi(STA)'
        :param assert_interface: 校验tab选项有无对应接口选项

        """
        self.access_menu('status.link_monitoring')
        self.agg_in(FunctionsLocators(self.page, self.locale, self.model).link_quality_history,
                    {'interface_tab': interface})
        self.page.locator('//input[@type="search"]').click(force=True)
        # 聚焦
        if assert_interface:
            tab = self.page.locator('.rc-virtual-list-holder-inner').text_content()
            assert interface in tab, f'{interface} not in tab'
            self.page.wait_for_timeout(1000)
            assert self.page.locator(
                '//div[@class="echarts-for-react "]').count() == 3, 'link monitoring page no echarts'
            #  校验吞吐 延迟
            interface_ = interface.replace('Wi-Fi(STA)', 'wlan-sta').replace(
                'Cellular', 'cellular1').replace('WAN1', 'wan1').replace('WAN2', 'wan2')
            speed_info = self.wait_for_response(f'name={interface_}&table=speed')
            assert speed_info != [], f'{interface} no speed data'
            delay_info = self.wait_for_response(f'name={interface_}&table=delay')
            assert delay_info != [], f'{interface} no delay data'
            if interface_.startswith('wan'):
                # 校验 丢包
                loss_info = self.wait_for_response(f'name={interface_}&table=loss')
                assert loss_info != [], f'{interface} no loss data'
            else:
                # 校验  信号强度
                signal_info = self.wait_for_response(f'name={interface_}&table=signal')
                assert signal_info != [], f'{interface} no signal data'
        else:
            assert interface not in self.page.locator(
                '.rc-virtual-list-holder-inner').text_content(), f'{interface} exit in tab'


class CellularSignal(BasePage):

    @allure.step('断言cellular历史信号')
    def assert_signal_history_info(self, sim='sim1', type_='5g', data_interval=15):
        """

        :param sim: 'sim1'|'sim2' 必有该卡的数据
        :param type_: '4g'|'5g' 必有该类型的数据
        :param data_interval: 单位秒， 默认15， 两条数据传的时间间隔
        :return:
        """
        device_path = "{}://{}".format(self.protocol, self.host)
        with self.page.expect_response(
                lambda response: f"{device_path}/api/v1/status/signal_history_info" == response.url) as response_info:
            self.access_menu('status.cellular_signal')
        data_list = response_info.value.json().get('result').get('signal_history_info')
        if data_list:
            assert self.page.locator(
                f'//div[@class="echarts-for-react "]').count() >= 4, 'cellular signal page not show signal echarts'
            data_time = ''
            x = False  # 跳过脏数据的时间
            sim = 1 if sim == 'sim1' else 2
            for data in data_list:
                if not data.get('network') and x:
                    x = False
                elif not data.get('network') and not x:
                    pass
                elif data.get('network') and not x:
                    data_time = data.get('timestamp')
                    x = True
                else:
                    b = datetime.strptime(data.get('timestamp'), "%Y-%m-%dT%H:%M:%S+0800")
                    a = datetime.strptime(data_time, "%Y-%m-%dT%H:%M:%S+0800")
                    assert (b - a).seconds == data_interval, 'the signal history info Collect interval error'
                    data_time = data.get('timestamp')
                assert data.get('sim') in (1, 2), 'the signal history info sim error'
                assert data.get('network') in ('3G', '4G', '5G', None), 'the signal history info network error'
                if data.get('network') == '5G':
                    assert data.get('dbm') <= 0 and isinstance(data.get('dbm'), int), f"now is {data.get('dbm')}"
                    assert data.get('ss_rsrp') is None or data.get('ss_rsrp') <= 0 and isinstance(
                        data.get('ss_rsrp'), int), f"now is {data.get('ss_rsrp')}"
                    assert data.get('ss_rsrq') is None or (data.get('ss_rsrq') <= 20 and data.get(
                        'ss_rsrq') >= -43), f"now is {data.get('ss_rsrq')}"  # 由于存在network有值但ss_sinr为null的情况，暂时这么处理
                    assert data.get('ss_sinr') is None or (data.get('ss_sinr') >= -23 and data.get(
                        'ss_sinr') <= 40), f"now is {data.get('ss_sinr')}"
                elif data.get('network') == '4G':
                    assert data.get('dbm') <= 0 and isinstance(data.get('dbm'), int)
                    assert data.get('rsrp') is None or data.get('rsrp') <= 0 and isinstance(data.get('rsrp'),
                                                                                            int), f"now is {data.get('rsrp')}"
                    assert data.get('rsrq') is None or (2.5 >= data.get('rsrq') >= -156), f"now is {data.get('rsrq')}"
                    assert data.get('sinr') is None or (-23 <= data.get('sinr') <= 40), f"now is {data.get('sinr')}"
                elif data.get('network') == '3G':
                    pass
                else:
                    pass
            for data in data_list:
                if data.get('sim') == sim and data.get('network') == type_.upper():
                    break
            else:
                raise Exception('the signal history not contain expect data')
        else:
            raise Exception('the signal history info Collect None')


class Clients(BasePage):

    @allure.step('断言clients状态')
    @loop_inspector('clients_status')
    def assert_status(self, ip_address: str, clients=None, filter_type=None, **kwargs):
        """
        :param clients: 'all'|'wired'|'wireless'
        :param filter_type: 'name'|'ip_address'|'mac_address'|'vlan'
        :param ip_address: str
        :param kwargs:
            name: str, 可以是'${value}'=='str' 等表达式
            mac_address: str, 可以是'${value}'=='str' 等表达式
            vlan: int, 可以是'${value}'=='str' 等表达式
            connection: str, 可以是'${value}'=='str' 等表达式
            traffic: str, 可以是'${value}'=='str' 等表达式
            traffic_unit: str, 可以是'${value}'=='str' 等表达式
            up: str, 可以是'${value}'=='str' 等表达式
            up_unit: str, 可以是'${value}'=='str' 等表达式
            down: str, 可以是'${value}'=='str' 等表达式
            down_unit: str, 可以是'${value}'=='str' 等表达式
            uptime: str, 可以是'${value}'=='str' 等表达式
            exist: '"${value}"=="None"'时校验不存在, 默认校验存在
        :return:
        """
        self.access_menu('status.clients')
        self.agg_in(FunctionsLocators(self.page, self.locale, self.model).clients,
                    {clients: "check", 'filter_type': filter_type})
        if kwargs:
            locators = FunctionsLocators(self.page, self.locale, self.model).clients_status(ip_address)
            return self.eval_locator_attribute(kwargs, locators=locators)

    @allure.step('获取clients状态')
    def get_status(self, name: str, keys: str or list or tuple) -> str or dict or None:
        """

        :param name: str,客户端ip
        :param keys: str or list or tuple , value
        :return: value or {'name1': value}
        """

        if name:
            clients_locators = FunctionsLocators(self.page, self.locale, self.model).clients_status(name)
            self.access_menu('status.clients')
            return self.get_text(keys, clients_locators)

    @allure.step('接口获取客户端信息')
    def get_clients_by_api(self) -> dict:
        """ 获取客户端的信息

        :return:
        """
        return self.api.get_status('clients')


class IpsecStatus(BasePage):

    @allure.step('断言ipsec状态')
    @loop_inspector('ipsec_status')
    def assert_status(self, name: str, **kwargs):
        """
        :param name: str
        :param kwargs:
            status: '"up" in "${value}"'|'"down" in "${value}"'
            uplink_interface: str, 'WAN1'|'WAN2'|'Cellular'|'Wi-Fi(STA)'| 可以是'${value}'=='str' 等表达式
            interface_address: str, ip|可以是'${value}'=='str' 等表达式
            remote_address: str, ip| 可以是'${value}'=='str' 等表达式
            avaliable_subnets: str, ip-ip| 可以是'${value}'=='str' 等表达式
            traffic: str,  可以是'${value}'=='str' 等表达式
            traffic_unit: str,  可以是'${value}'=='str' 等表达式
            last_connection_time: str,  可以是'${value}'=='str' 等表达式
            exist: '"${value}"=="None"'时校验不存在, 默认校验存在
        :return:
        """
        if kwargs:
            locators = FunctionsLocators(self.page, self.locale, self.model).ipsec_status(name)
            self.access_menu('status.vpn.ipsec')
            return self.eval_locator_attribute(kwargs, locators)

    @allure.step('获取ipsec状态')
    def get_status(self, name: str, keys: str or list or tuple) -> str or dict or None:
        """

        :param name: str, ipsec名称
        :param keys: str or list or tuple , value
        :return: value or {'name1': value}
        """
        if name:
            ipsec_status_locators = FunctionsLocators(self.page, self.locale, self.model).ipsec_status(name)
            self.access_menu('status.vpn.ipsec')
            return self.get_text(keys, ipsec_status_locators)

    @allure.step('接口获取ipsec信息')
    def get_ipsec_by_api(self) -> dict:
        """ 获取ipsec的信息

        :return:
        """
        return self.api.get_status('ipsec')


class L2tpStatus(BasePage):

    @allure.step('断言l2tp状态')
    @loop_inspector('l2tp_status')
    def assert_status(self, name: str, **kwargs):
        """
        :param name: str
        :param kwargs:
            status: '"up" in "${value}"'|'"down" in "${value}"'
            type: str, 可以是'${value}'=='str' 等表达式
            local_address: str, ip|可以是'${value}'=='str' 等表达式
            peer_address: str, ip| 可以是'${value}'=='str' 等表达式
            traffic: str,  可以是'${value}'=='str' 等表达式
            traffic_unit: str,  可以是'${value}'=='str' 等表达式
            last_connection_time: str,  可以是'${value}'=='str' 等表达式
            exist: '"${value}"=="None"'时校验不存在, 默认校验存在
        :return:
        """

        if kwargs:
            locators = FunctionsLocators(self.page, self.locale, self.model).l2tp_status(name)
            self.access_menu('status.vpn.l2tp')
            return self.eval_locator_attribute(kwargs, locators)

    @allure.step('获取l2tp状态')
    def get_status(self, name: str, keys: str or list or tuple) -> str or dict or None:
        """

        :param name: str,l2tp名称
        :param keys: str or list or tuple , value
        :return: value or {'name1': value}
        """

        if name:
            l2tp_status_locators = FunctionsLocators(self.page, self.locale, self.model).l2tp_status(name)
            self.access_menu('status.vpn.l2tp')
            return self.get_text(keys, l2tp_status_locators)

    @allure.step('接口获取l2tp信息')
    def get_l2tp_by_api(self) -> dict:
        """ 获取ipsec的信息

        :return:
        """
        return self.api.get_status('l2tp')


class PassthroughStatus(BasePage):

    @allure.step('断言passthrough状态')
    @loop_inspector('passthrough_status')
    def assert_status(self, **kwargs):
        """
        :param kwargs:
            status: str, 可以是'${value}'=='str' 等表达式
            passthrough_wan: str, 可以是'${value}'=='str' 等表达式
            passthrough_lan: str, 可以是'${value}'=='str' 等表达式
            passthrough_ip_mask: str, 可以是'${value}'=='str' 等表达式
            passthrough_gateway: str,  可以是'${value}'=='str' 等表达式
            passthrough_dns1: str,  可以是'${value}'=='str' 等表达式
            passthrough_dns2: str,  可以是'${value}'=='str' 等表达式
            passthrough_mac: str,  可以是'${value}'=='str' 等表达式
            address_allocation_status: str,  可以是'${value}'=='str' 等表达式
            lease_timeout: str,  可以是'${value}'=='str' 等表达式
            exist: '"${value}"=="None"'时校验不存在, 默认校验存在
        :return:
        """

        if kwargs:
            locators = FunctionsLocators(self.page, self.locale, self.model).passthrough_status
            self.access_menu('status.passthrough')
            return self.eval_locator_attribute(kwargs, locators)

    @allure.step('获取passthrough状态')
    def get_status(self, keys: str or list or tuple) -> str or dict or None:
        """

        :param keys: str or list or tuple , value
        :return: value or {'name1': value}
        """

        if keys:
            locators = FunctionsLocators(self.page, self.locale, self.model).passthrough_status
            self.access_menu('status.passthrough')
            return self.get_text(keys, locators)


class Events(BasePage):

    @allure.step('检查事件是否存在并校验事件内容')
    def assert_events_by_api(self, start=None, end=None, event_types='login_success', least: int or dict or None = None):
        """

        :param start: str, ex:'2023-12-01'
        :param end:  str, ex:'2023-12-01'
        :param event_types: str, login_success| login_fail| config_change| cell_type_threshold| detection_success|
                            detection_fail| wan1_connect| wan1_disconnect| wan1_to_sim1| sim1_to_wan1|
                            wan1_to_wan2| wan2_to_wan1| ipsec_connect| ipsec_disconnect| l2tp_connect|
                            l2tp_disconnect| wan2_to_lan1| lan1_to_wan2| reboot| upgrade
                            支持多个，多个之间用逗号隔开
        :param least: 最少出现的次数，为None时，不对数量做校验，为int时，对所有类型的总数量做总计判断，为字典时可以针对某个类型数量做判断
                      None|10|{'login_success': 1, 'login_fail': 2}
        :return:
        """
        self.api.assert_events(start, end, event_types, least, self.language)

    @allure.step('清除事件')
    def clear(self):
        """
        :return:
        """
        url = f"{self.api.device_path}{self.api.path_url.get('events_url')}?limit=20&page=-1"
        with self.page.expect_response(lambda response: url == response.url) as response_info:
            self.agg_in(FunctionsLocators(self.page, self.locale, self.model).events,
                        {'clear_events': True, 'action_confirm': True})
            total = response_info.value.json().get('total')
            assert not total, f'event clear failed, now event number is {total}'

    @allure.step('导出事件')
    def export(self, export_events: dict or str):
        """

        export_events: dict, {'file_path': $file_path, 'file_name': $file_name} 或者文件夹
        :return:
        """
        self.access_menu('status.events')
        self.agg_in(FunctionsLocators(self.page, self.locale, self.model).events, {'export_events': export_events})

    @allure.step('查找事件')
    def find(self, event_time=('', ''), event_type='login_ok', limit=100, assert_api=False):
        """

        :param event_time: (${start_time}, ${end_time}) ('2022-09-01', '2022-09-01'), 开始时间和结束时间必须同时存在
        :param event_type: 'login_ok'|'login_fail'|'config'|'cpu_high'|'memory_high'|'vpn_state'|'uplink_state'|'uplink_switch'|
                        'wan2_lan1_s'|'upgrade'|'reboot'|'uplink_detect'|'cellular_flow', 多个用逗号连接
        :param limit: 10, 20, 50, 100
        :param assert_api: True | False，  开启后直接对API做参数校验，还有结果
        :return:
        """
        start_time, end_time = event_time[0], event_time[1]
        start = f"start={int(time.mktime(time.strptime(f'{start_time} 00:00:00', '%Y-%m-%d %H:%M:%S')))}" if start_time else ''
        end = f"end={int(time.mktime(time.strptime(f'{end_time} 23:59:59', '%Y-%m-%d %H:%M:%S')))}" if end_time else ''
        type_ = f'type={event_type}' if event_type else ''
        param = '&'.join([f'page=-1', 'limit=100', type_, start, end]).strip('&')
        url = f'{self.api.device_path}{self.api.path_url.get("events_url")}?{param}'
        self.access_menu('status.events')
        with self.page.expect_response(lambda response: url == response.url, timeout=120000) as response_info:
            self.agg_in(FunctionsLocators(self.page, self.locale, self.model).events,
                        {'event_type': event_type.split(','), 'page_limit': limit, 'start_time': start_time,
                         'end_time': end_time})
        if assert_api:
            all_events = response_info.value.json().get('events')
            assert response_info.value.status == 200, "events api status error"
            assert len(all_events) <= limit, "events limit status error"


class Logs(BasePage):

    @allure.step('查询日志')
    def find(self, level='all', lines=50, search=True, reset=False, assert_api=False, **kwargs):
        """查询日志

        :param level: 查询日志的级别, str, 'all'| 'error'| 'emergency'| 'serious'| 'warning'| 'alarm'| 'notice'|
                        'information'| 'debug'
        :param lines: 显示行数, int, 50| 100| 200| 500
        :param search: 是否点击查询 True| False 点击| 不点击
        :param reset: 是否重置查询 True| False 点击| 不点击
        :param assert_api: True | False，  开启后直接对API做参数校验，还有结果
        :param kwargs:
        :return:
        """
        all_level = {'all': -1, 'error': 0, 'emergency': 1, 'serious': 2, 'warning': 3, 'alarm': 4, 'notice': 5,
                     'information': 6, 'debug': 7}
        self.access_menu('status.logs')
        url = f'{self.api.device_path}{self.api.path_url.get("logs_url")}?lines={lines}&level={all_level.get(level)}&' \
              f'keys={kwargs.get("key")}' if kwargs and kwargs.get('key') else \
            f'{self.api.device_path}{self.api.path_url.get("logs_url")}?lines={lines}&level={all_level.get(level)}'
        with self.page.expect_response(
                lambda response: url == response.url) as response_info:
            self.agg_in(FunctionsLocators(self.page, self.locale, self.model).logs,
                        {'level': level, 'line_limit': lines, 'key': kwargs.get('key'), 'search': search,
                         'reset': reset})
        if assert_api:
            assert response_info.value.status == 200, "logs api status error"
            assert len(response_info.value.json().get('result')) <= lines, "logs limit status error"

    @allure.step('清除日志')
    def clear(self):
        """
        :return:
        """
        url = f"{self.api.device_path}/api/v1/syslog/clean?type=syslog"
        with self.page.expect_response(lambda response: url == response.url) as response_info:
            self.agg_in(FunctionsLocators(self.page, self.locale, self.model).logs,
                        {'clear_logs': True, 'action_confirm': True})
        assert response_info.value.json().get('result') == 'ok', 'logs clear failed, clean api response error'

    @allure.step('导出日志')
    def export(self, **kwargs):
        """

        :param kwargs:
            download_logs: dict, {'file_path': $file_path, 'file_name': $file_name}
            diagnostic_logs: dict, 下载诊断日志, {'file_path': $file_path, 'file_name': $file_name}
        :return:
        """
        self.access_menu('status.logs')
        self.agg_in(FunctionsLocators(self.page, self.locale, self.model).logs, kwargs)

    @allure.step('查找事件')
    def refresh(self, refresh='manual_refresh', reload=False, assert_api=False):
        """刷新日志

        :param refresh: 刷新频率, str or int, 'manual_refresh'| 5| 10| 15|60
        :param reload: 是否点击刷新按钮 True| False 点击| 不点击
        :param assert_api: True | False，  开启后直接对API做参数校验，还有结果
        :return:
        """

        self.access_menu('status.logs')
        url = f"{self.api.device_path}{self.api.path_url.get('logs_url')}?lines=50&level=-1"
        with self.page.expect_response(lambda response: url == response.url, timeout=90000) as response_info:
            self.agg_in(FunctionsLocators(self.page, self.locale, self.model).logs,
                        {'line_limit': 50, 'reset': True, 'refresh': refresh, 'reload': reload})
            startime = datetime.now()
            if refresh != 'manual_refresh':
                self.wait_for_response(self.api.path_url.get('logs_url'), timeout=90000)
                endtime = datetime.now()
                timedel = (endtime - startime).seconds
                assert timedel <= int(refresh) + 4, 'assert logs api response timedelta error'
        if assert_api:
            assert response_info.value.status == 200, "logs api status error"
            assert response_info.value.json().get('result'), 'logs api response error'
        self.agg_in(FunctionsLocators(self.page, self.locale, self.model).logs, {'refresh': 'manual_refresh'})


class LanOrLocalNetwork(BasePage):

    @allure.step('配置lan')
    def config(self, **kwargs):
        """

        :param kwargs:
           lan_resource:
                [($action, **kwarg)] ex: [('delete_all', )],
                [('delete', '10.5.24.97')]
                [('edit', $old, $new)]
                [('add', {'name': 'test', 'ip_address_mask': ''})]
                action: add|delete|delete_all|edit|exist
                    add parameters:
                        name: str
                        ip_mode: 'check'|'uncheck'
                        vlan_only_mode: 'check'|'uncheck'
                        standard: 'check'|'uncheck'
                        guest: 'check'|'uncheck'
                        vlan: int
                        ip_address_mask: str, '192.168.2.1/24'
                        dhcp_server: 'enable'|'disable'
                        dhcp_ip_range_start_ip: str, '192.168.2.1'
                        dhcp_ip_range_end_ip: str, '192.168.2.254'
                        ipv6: 'disable'| 'auto'| 'static_ip'
                        ipv6_address: str, '2001:db8::1'
                        ipv6_prefix_length: int
                        save: True, False
                        cancel: True, False
                        text_messages: str or list
                        tip_messages: str or list
        :return:
        """
        if self.model == 'EAP600':
            self.access_menu('config.lan')
        else:
            self.access_menu('local_network')
            result = []
            for value in kwargs.get('lan_resource')[0]:
                if isinstance(value, dict) and value.get('ip_address_mask'):
                    value_ = value.pop('ip_address_mask')
                    value.update({'ip_address': value_.split('/')[0], 'mask': value_.split('/')[1]})
                result.append(value)
            if result:
                kwargs.update({'lan_resource': [tuple(result)]})
        self.agg_in(FunctionsLocators(self.page, self.locale, self.model).lan_or_localnetwork, kwargs)


class Internet(BasePage):

    @allure.step('配置internet')
    def config(self, **kwargs):
        """
        配置internet
        :param kwargs:
            uplink_table:
            [($action, **kwarg)] ex: [('delete_all', )],
            [('delete', '$interface')]
            [('edit', '$interface', $new)]
            [('add', {'name': '$interface', 'ip_address_mask': ''})]
            action: add|delete|delete_all|edit|exist
                    name: str, 'WAN2'| 'Wi-Fi(STA)'
                    (当对接口进行编辑时, 不传入name参数, ex:[('edit', $interface, $new)], 删除同理
                    $interface: 'WAN1'|'WAN2'|'Wi-Fi(STA)'| 'Cellular')
                以下为WAN1/WAN2和Wi-Fi(STA)公共参数:
                    ipv4_type: 'dhcp'|'static_ip'| 'pppoe'
                    ipv4_address: str, ip, ex:'192.168.2.100'
                    mask: str, mask, ex:'255.255.255.0'
                    ipv4_gateway_address: str, ex:'192.168.2.1'
                    main_dns: str, ex:'223.5.5.5'
                    secondary_dns: str, ex:'223.5.5.5'
                    mtu: int, ex:1500
                以下为配置WAN1/WAN2独有参数:
                    pppoe_user_name: str,
                    pppoe_password: str,
                    local_ip_address: str,
                    remote_ip_address: str,
                    ipv6_type: 'dhcp'|'static_ip'| 'auto'
                    ipv6_address: str, ip, ex:'2001:db8::1'
                    prefix_length: str, ex:'64'
                    ipv6_gateway_address: str, ex:'2001:db8::1'
                    main_ipv6_dns: str, ex:'2001:db8::1'
                    secondary_ipv6_dns: str, ex:'2001:db8::1'
                以下为配置Wi-Fi(STA)独有参数:
                    band: '2.4g'|'5g'
                    ssid: str
                    security: 'open'|'wpa_psk'|'wpa2_psk'| 'wpa_wpa2_psk'
                    encryption: 'ccmp'|'ccmp_tkip'
                    wlan_password: str
                以下为配置Cellular独有参数:
                (编辑Cellular时, 传参方式ex:[('edit', 'Cellular', {'work_mode': $work_mode, 'sim1':**kwargs,
                'sim2':**kwargs})])
                    work_mode: 'only_sim1'|'only_sim2'|'dual_mode'
                    primary_card: 'sim1'|'sim2'
                    cellular_mtu_mode: 'auto'|'manual'
                    cellular_mtu_input: int, ex:1500
                    sim1/sim2:dict
                        dialing_parameters: 'auto'|'manual'
                        service_type: 'auto'| '2g'| '3g'| '4g'| '5g_sa'| '4g&5g'
                        5g_type: service_type=auto时有'sa'|'nsa'| 'sa_nsa',
                                service_type=4g&5g时有'sa_nsa_lte'|'nsa_lte'|'sa_lte', 其他值无该参数
                        pin_code: str
                        ims: 'auto'|'enable'| 'disable'
                        ip_type: 'ipv4'|'ipv6'| 'ipv4&ipv6'
                        apn: str
                        authentication: 'auto'|'pap'| 'chap'| 'ms_chap'| 'ms_chapv2'
                        username: str
                        password: str
                以下为所有接口的公共参数:
                    status: 'enable'|'disable'
                    nat: 'check'|'uncheck'
                    save: True, False or dict
                    cancel: True, False or dict
                    text_messages: str or list
                    tip_messages: str or list
            policy:
                [('policy', {'usage_traffic': $param, 'sim1': **kwargs, 'sim2': **kwargs})]})]
                sim1/sim2: dict
                    threshold_enable: 'enable'|'disable'
                    threshold_input: int
                    threshold_unit: 'mb'|'gb'|'kb'
                    monthly_reset_day: int, 1-31
                    action: 'notification'| 'only_cloud_management_traffic'
                    usage_of_the_month: int, 流量校准时填入
                    usage_of_the_month_unit: 'mb'|'gb'|'kb', 流量校准时填入
                abnormal_card_switching_time: int, seconds
                reuse_the_primary_card: str or list, 'usage'| 'time'| 'date'
                usage_traffic: int
                usage_traffic_unit: 'mb'|'gb'
                using_time: float, hours, 0.5-240
                switching_day_of_month, int, 1-31
            link_detection: 'enable'|'disable'
            detection_address_1: str
            detection_address_2: str
            link_backup: 'check'|'uncheck'
            failover_mode: 'immediately_switch'| 'delayed_switch'| 'do_not_switch'
            delay_number: int, 5-60s
            load_balancing: 'enable'|'disable'
            save: True, False or dict
            reset: True, False or dict
            text_messages: str or list
            tip_messages: str or list
        :return:
        """

        def get_value(value):
            def get_sim1_sim2(value_):
                if isinstance(value_, dict):
                    sim1, sim2 = {'sim1': value_.get('sim1')}, {'sim2': value_.get('sim2')}
                    for param in [sim1, sim2]:
                        if param:
                            for k, v in param.items():
                                if v:
                                    value_.pop(k)
                                    if value_.get('work_mode') == 'dual_mode':
                                        v.update({f'tab': True})
                                    elif 'usage_of_the_month' in v.keys() or 'usage_traffic_unit' in v.keys():
                                        v.update({f'modify': True, f'usage_of_the_month_confirm': True})
                                    value_.update({f"{k}_{key}": value for key, value in param.get(k).items()})
                return value_

            if isinstance(value, tuple):
                result = []
                [result.append(i) for i in value]
                if len(value) > 1:
                    if 'edit' in result[0]:
                        values = result[2]
                        result[2] = get_sim1_sim2(values)
                    else:
                        values = result[1]
                        result[1] = get_sim1_sim2(values)
                    return [tuple(result)]

        for i in ['uplink_table', 'policy']:
            params = kwargs.get(i)
            if params:
                kwargs.pop(i)
                for value in params:
                    get_value(value)
            kwargs.update({i: params})
        self.access_menu('internet')
        self.agg_in(FunctionsLocators(self.page, self.locale, self.model).internet, kwargs)


class InboundRules(BasePage):

    @allure.step('配置入站规则')
    def config(self, **kwargs):
        """
        :param kwargs:
           inbound_rules:
                [($action, **kwarg)] ex: [('delete_all', )],
                [('delete', '10.5.24.97')]
                [('edit', $old, $new)]
                [('add', {'name': 'test', 'ip_address_mask': ''})]
                [('insert_row_up, 'test', {'name':'test1', 'protocol':'TCP'})] insert_row_up| insert_row_down, 向上插入|向下插入
                [('edit', 'Default', {'permit': True})]默认规则编辑
                action: add|delete|delete_all|edit|exist|insert_row_up| insert_row_down
                    add parameters:
                        name: str
                        status: 'enable'|'disable'
                        interface: 'WAN1'|'WAN2'|'Cellular'|'WI-Fi(STA)'
                        protocol: 'any'|'tcp'|'udp'|'icmp'|'custom'
                        protocol_input: int
                        source: 'any'|'custom'
                        source_input: str, '192.168.2.1/24'
                        src_port: 'any'|'custom'
                        src_port_input: int
                        destination: 'any'|'custom'
                        destination_input: str, '192.168.2.1/24'
                        dst_port: 'any'|'custom'
                        dst_port_input: int
                        permit: True|False
                        deny: True|False
                        save: True, False
                        cancel: True, False
                        text_messages: str or list
                        tip_messages: str or list
        :return:
        """

        self.access_menu('security.firewall.inbound_rules')
        self.agg_in(FunctionsLocators(self.page, self.locale, self.model).inbound_rules, kwargs)


class outboundRules(BasePage):

    @allure.step('配置出站规则')
    def config(self, **kwargs):
        """
        :param kwargs:
           outbound_rules:
                [($action, **kwarg)] ex: [('delete_all', )],
                [('delete', '10.5.24.97')]
                [('edit', $old, $new)]
                [('add', {'name': 'test', 'ip_address_mask': ''})]
                [('insert_row_up, 'test', {'name':'test1', 'protocol':'TCP'})] insert_row_up| insert_row_down, 向上插入|向下插入
                [('edit', 'Default', {'permit': True})]默认规则编辑
                action: add|delete|delete_all|edit|exist|insert_row_up| insert_row_down
                    add parameters:
                        name: str
                        status: 'enable'|'disable'
                        interface: 'WAN1'|'WAN2'|'Cellular'|'WI-Fi(STA)'
                        protocol: 'any'|'tcp'|'udp'|'icmp'|'custom'
                        protocol_input: int
                        source: 'any'|'custom'
                        source_input: str, '192.168.2.1/24'
                        src_port: 'any'|'custom'
                        src_port_input: int
                        destination: 'any'|'custom'
                        destination_input: str, '192.168.2.1/24'
                        dst_port: 'any'|'custom'
                        dst_port_input: int
                        permit: True|False
                        deny: True|False
                        save: True, False
                        cancel: True, False
                        text_messages: str or list
                        tip_messages: str or list
        :return:
        """

        self.access_menu('security.firewall.outbound_rules')
        self.agg_in(FunctionsLocators(self.page, self.locale, self.model).outbound_rules, kwargs)


class PortForwarding(BasePage):

    @allure.step('配置端口转发')
    def config(self, **kwargs):
        """
        :param kwargs:
           port_forwarding:
                [($action, **kwarg)] ex: [('delete_all', )],
                [('delete', '
                [($action, **kwarg)] ex: [('delete_all', )],
                [('delete', '10.5.24.97')]
                [('edit', $old, $new)]
                [('add', {'name': 'test', 'ip_address_mask': ''})]
                [('edit', 'Default', {'permit': True})]默认规则编辑
                action: add|delete|delete_all|edit|exists
                    add parameters:
                        name: str
                        status: 'enable'|'disable'
                        interface: 'WAN1'|'WAN2'|'Cellular'|'WI-Fi(STA)'
                        protocol: 'tcp'|'udp'|'tcp&udp'
                        public_port: int
                        local_address: str, '192.168.2.100'
                        local_port: int
                        save: True, False
                        cancel: True, False
                        text_messages: str or list
                        tip_messages: str or list
        :return:
        """

        self.access_menu('security.firewall.port_forwarding')
        self.agg_in(FunctionsLocators(self.page, self.locale, self.model).port_forwarding, kwargs)


class Nat(BasePage):

    @allure.step('配置端口转发')
    def config(self, **kwargs):
        """
        :param kwargs:
            input_name_query: str
            input_ip_query: str
            input_port_query: str
            reset: True, False
            nat:
                [($action, **kwarg)] ex: [('batch_delete',['test123'])],
                                        [('batch_delete','all')],
                [('edit', $old, $new)]
                [('add', {'name': 'test', 'ip_address_mask': ''})]
                [('insert_row_up, 'test', {'name':'test1', 'protocol':'TCP'})] insert_row_up| insert_row_down, 向上插入|向下插入
                action: add|batch_delete|edit|exist|insert_row_up| insert_row_down
                    add parameters:
                        name: str
                        status: 'enable'|'disable'
                        type: 'SNAT'|'DNAT'
                        protocol: 'tcp'|'udp'|'tcp&udp'| 'any'
                        source: 'any'|'custom'
                        source_input: str,
                        src_port: 'any'|'custom'
                        src_port_input: int
                        destination: 'any'|'custom'
                        destination_input: str,
                        dst_port: 'any'|'custom'
                        dst_port_input: int
                        converted_address: str,
                        converted_port: 'any'|'custom'
                        converted_port_input: int
                        save: True, False
                        cancel: True, False
                        text_messages: str or list
                        tip_messages: str or list
        :return:
        """

        self.access_menu('security.firewall.nat')
        self.agg_in(FunctionsLocators(self.page, self.locale, self.model).nat, kwargs)


class MacAddressFilter(BasePage):
    @allure.step('配置mac地址过滤')
    def config(self, **kwargs):
        """
        :param kwargs:
            unlimited: 'check'|'uncheck'
            blacklist: 'check'|'uncheck'
            whitelist: 'check'|'uncheck'
            save: True, False, dict
            reset: True, False
            mac_address_list:
                [($action, **kwarg)] ex: [('delete','test123')],
                                        [('delete_all',)],
                [('edit', $old, $new)]
                [('add', {'name': 'test', 'ip_address_mask': ''})]
                action: add|delete|edit|exist|delete_all
                    add parameters:
                        mac_address: str
                        status: 'enable'|'disable'
                        description: str
                        save: True, False, dict
                        cancel: True, False
                        text_messages: str or list
                        tip_messages: str or list
        :return:
        """

        self.access_menu('security.firewall.mac_address_filter')
        self.agg_in(FunctionsLocators(self.page, self.locale, self.model).mac_address_filter, kwargs)


class DominNameFilter(BasePage):
    @allure.step('配置域名过滤')
    def config(self, **kwargs):
        """
        :param kwargs:
            unlimited: 'check'|'uncheck'
            blacklist: 'check'|'uncheck'
            whitelist: 'check'|'uncheck'
            save: True, False, dict
            reset: True, False
            domin_name_list:
                [($action, **kwarg)] ex: [('delete','test123')],
                                        [('delete_all',)],
                [('edit', $old, $new)]
                [('add', {'name': 'test', 'ip_address_mask': ''})]
                action: add|delete|edit|exist|delete_all
                    add parameters:
                        domains: str
                        description: str
                        save: True, False, dict
                        cancel: True, False
                        text_messages: str or list
                        tip_messages: str or list
        :return:
        """

        self.access_menu('security.firewall.domin_name_filter')
        self.agg_in(FunctionsLocators(self.page, self.locale, self.model).domin_name_filter, kwargs)


class PolicyBasedRouting(BasePage):
    @allure.step('配置策略路由')
    def config(self, **kwargs):
        """
        :param kwargs:
           policy_based_routing:
                [($action, **kwarg)] ex: [('delete_all', )],
                [('delete', '
                [($action, **kwarg)] ex: [('delete_all', )],
                [('delete', '10.5.24.97')]
                [('edit', $old, $new)]
                [('add', {'name': 'test', 'ip_address_mask': ''})]
                [('insert_row_up, 'test', {'name':'test1', 'protocol':'TCP'})] insert_row_up| insert_row_down, 向上插入|向下插入
                [('edit', 'Default', {'permit': True})]默认规则编辑
                action: add|delete|delete_all|edit|exists|insert_row_up| insert_row_down
                    (该页面最好不要使用模糊查找, 页面会出现confirm.is_visible() is not True的情况)
                    add parameters:
                        name: str
                        status: 'enable'|'disable'
                        protocol: 'tcp'|'udp'|'any'| 'icmp'| 'custom'
                        protocol_input: int
                        source: 'any'|'custom'
                        source_input: str,
                        src_port: 'any'|'custom'
                        src_port_input: int
                        destination: 'any'|'custom'
                        destination_input: str,
                        dst_port: 'any'|'custom'
                        dst_port_input: int
                        output: 'WAN1'|'WAN2'|'Cellular'|'WI-Fi(STA)'
                        forced_forwarding: 'check'|'uncheck'
                        save: True, False
                        cancel: True, False
                        text_messages: str or list
                        tip_messages: str or list
        :return:
        """

        self.access_menu('security.policy_based_routing')
        self.agg_in(FunctionsLocators(self.page, self.locale, self.model).policy_based_routing, kwargs)


class TrafficShaping(BasePage):
    @allure.step('配置流量整形')
    def config(self, **kwargs):
        """
        :param kwargs:
            uplinlk_bandwidth:
                [('edit', $interface, $new)]
                action: edit
                    edit parameters:
                        up_bandwidth: int
                        up_bandwidth_unit: 'Kbps'|'Mbps'
                        down_bandwidth: int
                        down_bandwidth_unit: 'Kbps'|'Mbps'
                        save: True, False
                        cancel: True, False
                        text_messages: str or list
                        tip_messages: str or list
            shaping_rules:
                [($action, **kwarg)] ex: [('delete_all', )],
                [('delete', '10.5.24.97')]
                [('edit', $old, $new)]
                [('add', {'name': 'test', 'ip_address_mask': ''})]
                [('insert_row_up, 'test', {'name':'test1', 'protocol':'TCP'})] insert_row_up| insert_row_down, 向上插入|向下插入
                action: add|delete|delete_all|edit|exist|insert_row_up| insert_row_down
                    (该页面最好不要使用模糊查找, 页面会出现confirm.is_visible() is not True的情况)
                    add parameters:
                        name: str
                        status: 'enable'|'disable'
                        protocol: 'any'|'tcp'|'udp'|'icmp'|'custom'
                        protocol_input: int
                        source: 'any'|'custom'
                        source_input: str,
                        src_port: 'any'|'custom'
                        src_port_input: int
                        destination: 'any'|'custom'
                        destination_input: str,
                        dst_port: 'any'|'custom'
                        dst_port_input: int
                        priority: 'highest'|'high'|'medium'|'low'| 'lowest'
                        dscp_tags: 'no_dscp'| '10'| '12'| '14'| '18'| '20'| '22'| '26'| '28'| '30'| '34'|
                                    '36'| '38'| '0'| '8'| '16'| '24'| '32'| '40'| '46'| '48'| '56'| '44'
                        limit_bandwidth_up: int,
                        limit_bandwidth_up_unit: 'Kbps'|'Mbps'
                        limit_bandwidth_down: int,
                        limit_bandwidth_down_unit: 'Kbps'|'Mbps'
                        reserved_bandwidth_up: int,
                        reserved_bandwidth_up_unit: 'Kbps'|'Mbps'
                        reserved_bandwidth_down: int,
                        reserved_bandwidth_down_unit: 'Kbps'|'Mbps'
                        save: True, False
                        cancel: True, False
                        text_messages: str or list
                        tip_messages: str or list
        :return:
        """

        self.access_menu('security.traffic_shaping')
        self.agg_in(FunctionsLocators(self.page, self.locale, self.model).traffic_shaping, kwargs)


class IpsecVpn(BasePage):

    @allure.step("编辑ipsec VPN")
    def config(self, **kwargs):
        """
        :param kwargs:
            ipsec_vpn:
                [($action, **kwarg)] ex: [('delete_all', )],
                [('delete', '10.5.24.97')]
                [('edit', $old, $new)]
                [('add', {'name': 'test', 'ip_address_mask': ''})]
                action: add|delete|delete_all|edit|exist
                    add parameters:
                        name: str
                        status: 'enable'|'disable'
                        ike_version: 'ikev1'|'ikev2'
                        negotiation_mode: 'main_mode'|'agressive_mode'
                        pre_shared_key: str
                        uplink_interface: str, 'WAN1'|'WAN2'|'Wi-Fi(STA)'| 'Cellular'
                        peer_address: str, ip or domain name
                        tunnel_mode: 'tunnel'|'transmission'
                        local_subnet: list, ['192.168.2.0',], 最多支持四个子网
                        remote_subnet: list, ['192.168.2.0',], 最多支持四个子网
                        local_identity: 'auto'|'ip_address'|'fqdn'|'user_fqdn'
                        local_identity_id: str
                        peer_identity: 'auto'|'ip_address'|'fqdn'|'user_fqdn'
                        peer_identity_id: str
                        ike_policy_encryption: 'AES128'|'AES192'|'AES256'|'3DES'|'DES'
                        ike_policy_authentication: 'SHA1'|'SHA2-256'|'SHA2-384'|'SHA2-512'|'MD5'
                        ike_policy_dh_groups: int, 1|2|5|14|15|16|19|20|21|24
                        ike_policy_lifetime: int, 60-86400
                        ike_policy_peer_status_detect: 'enable'|'disable'
                        ike_policy_dpd_interval: int, 1-60
                        ike_policy_dpd_timeout: int, 10-3600
                        ipsec_policy_security_protocol: 'ESP'|'AH'
                        ipsec_policy_encryption: 'AES128'|'AES192'|'AES256'|'3DES'|'DES'
                        ipsec_policy_authentication: 'SHA1'|'SHA2-256'|'SHA2-384'|'SHA2-512'|'MD5'
                        ipsec_policy_pfs_groups: str or int, 'OFF'|1|2|5|14|15|16|19|20|21|24
                        ipsec_policy_lifetime: int, 60-86400
                        save: True, False, dict
                        cancel: True, False, dict
                        text_messages: str or list
                        tip_messages: str or list
        :return:
        """
        self.access_menu('vpn.ipsec_vpn')
        self.agg_in(FunctionsLocators(self.page, self.locale, self.model).ipsec_vpn, kwargs)


class L2tpVpnServer(BasePage):

    @allure.step("编辑L2tp VPN Server")
    def config(self, **kwargs):
        """
        :param kwargs:
                status: 'enable'|'disable'
                uplink_interface: 'WAN1'|'WAN2'|'Wi-Fi(STA)'| 'Cellular'
                vpn_connection_address: str, ip or domain name
                ip_pool_start: str, '10.10.10.1'
                ip_pool_end: str, '10.10.10.250'
                username: str
                password: str
                authentication_mode: 'auto'|'pap'|'chap'
                enable_tunnel_verification: 'check'| 'uncheck'
                server_name: str
                tunnel_verification_key: str
                save: True, False, dict
                cancel: True, False, dict
                text_messages: str or list
                tip_messages: str or list
        :return:
        """
        self.access_menu('vpn.l2tp_vpn.server')
        self.agg_in(FunctionsLocators(self.page, self.locale, self.model).l2tp_vpn, kwargs)


class L2tpVpnClient(BasePage):

    @allure.step("编辑L2tp VPN Client")
    def config(self, **kwargs):
        """
        :param kwargs:
            l2tp_client:
                [($action, **kwarg)] ex: [('delete_all', )],
                [('delete', '10.5.24.97')]
                [('edit', $old, $new)]
                [('add', {'name': 'test', 'ip_address_mask': ''})]
                action: add|delete|delete_all|edit|exist
                    add parameters:
                        name: str
                        status: 'enable'|'disable'
                        uplink_interface: str, 'WAN1'|'WAN2'|'Wi-Fi(STA)'| 'Cellular'
                        server_address: str, ip or domain name
                        authentication_mode: 'auto'|'pap'|'chap'
                        enable_tunnel_verification: 'check'| 'uncheck'
                        server_name: str
                        username: str
                        password: str
                        tunnel_verification_key: str
                        save: True, False, dict
                        cancel: True, False, dict
                        text_messages: str or list
                        tip_messages: str or list
        :return:
        """
        self.access_menu('vpn.l2tp_vpn.client')
        self.agg_in(FunctionsLocators(self.page, self.locale, self.model).l2tp_vpn, kwargs)


class VxlanVpn(BasePage):

    @allure.step("编辑Vxlan VPN")
    def config(self, **kwargs):
        """
        :param kwargs:
            vxlan_vpn:
                [($action, **kwarg)] ex: [('delete_all', )],
                [('delete', '10.5.24.97')]
                [('edit', $old, $new)]
                [('add', {'name': 'test', 'ip_address_mask': ''})]
                action: add|delete|delete_all|edit|exist
                    add parameters:
                    name: str
                    status: 'enable'|'disable'
                    uplink_interface: str, 'WAN1'|'WAN2'|'Wi-Fi(STA)'| 'Cellular'
                    peer_address: str, ip or domain name
                    vni: int, 1-16777215
                    local_subnets: str, '192.168.100.1/24(Default)' or '192.168.100.1/24' or 'Default'
        """
        self.access_menu('vpn.vxlan_vpn')
        self.agg_in(FunctionsLocators(self.page, self.locale, self.model).vxlan_vpn, kwargs)


class InterfaceManagement(BasePage):
    @allure.step('配置接口管理')
    def config(self, **kwargs):
        """
        :param kwargs:
            interface_management:
                [($action, **kwarg)] e
                [('edit', $old, $new)]
                action: edit|exist
                    edit parameters:
                        status: 'enable'|'disable'
                        network: 'all'| str
                        link_rate: 'auto'| 'full_1000mbps_duplex'| 'full_100mbps_duplex'| 'full_10mbps_duplex'|
                                    'half_100mbps_duplex'| 'half_10mbps_duplex'
                        save: True, False
                        cancel: True, False
                        text_messages: str or list
                        tip_messages: str or list
        :return:
        """
        self.access_menu('services')
        self.agg_in(FunctionsLocators(self.page, self.locale, self.model).interface_management,
                    {**{'expand': 'expand'}, **kwargs})


class DhcpServer(BasePage):
    @allure.step('配置Dhcp Server')
    def config(self, **kwargs):
        """
        :param kwargs:
            dhcp_server:
                [($action, **kwarg)] e
                [('edit', $old, $new)]
                action: edit|exist
                    edit parameters:
                        status: 'enable'|'disable'
                        dhcp_ip_range: ex: '192.168.2.2-192.168.2.254'
                        lease: '1_day'|'1_hour'|'1_week'|'12_hours'|'6_hours'
                        dns: 'auto'|'manual'
                        main_dns: str,
                        secondary_dns: str,
                        save: True, False
                        cancel: True, False
                        text_messages: str or list
                        tip_messages: str or list
        :return:
        """
        if kwargs and kwargs.get('dhcp_server'):
            param = kwargs.pop('dhcp_server')
            result = []
            for value in param:
                result_ = []
                for value_ in value:
                    if isinstance(value_, dict) and value_.get('dhcp_ip_range'):
                        ip_range = value_.pop('dhcp_ip_range')
                        value_.update({'dhcp_ip_range_start': ip_range.split('-')[0],
                                       'dhcp_ip_range_end': ip_range.split('-')[1]})
                    result_.append(value_)
                result.append(tuple(result_))
            kwargs.update({'dhcp_server': result})
        self.access_menu('services')
        self.agg_in(FunctionsLocators(self.page, self.locale, self.model).dhcp_server,
                    {**{'expand': 'expand'}, **kwargs})


class DnsServer(BasePage):
    @allure.step('配置Dns Server')
    def config(self, **kwargs):
        """
        :param kwargs:
            dns_server1: str,
            dns_server2: str,
            save: True, False
            reset: True, False
            text_messages: str or list
            tip_messages: str or list
        :return:
        """
        self.access_menu('services')
        self.agg_in(FunctionsLocators(self.page, self.locale, self.model).dns_server,
                    {**{'expand': 'expand'}, **kwargs})


class FixedAddressList(BasePage):
    @allure.step('配置固定地址列表')
    def config(self, **kwargs):
        """
        :param kwargs:
            network: 'all_network'| str
            filter_select: 'ip_address'|'mac_address'|'clients'
            filter_input: str
            fixed_address_list:
                [($action, **kwarg)] ex: [('delete_all', )],
                [('delete', '10.5.24.97')]
                [('edit', $old, $new)]
                [('add', {'name': 'test', 'ip_address_mask': ''})]
                action: add|delete|delete_all|edit|exist
                    add parameters:
                        network: str
                        mac_address: str
                        ip_address: str
                        clients: str
                        save: True, False, dict
                        cancel: True, False, dict
                        text_messages: str or list
                        tip_messages: str or list
        :return:
        """
        self.access_menu('services')
        self.agg_in(FunctionsLocators(self.page, self.locale, self.model).fixed_address_list,
                    {**{'expand': 'expand'}, **kwargs})


class StaticRoutes(BasePage):
    @allure.step('配置静态路由')
    def config(self, **kwargs):
        """
        :param kwargs:
            static_routes:
                [($action, **kwarg)] ex: [('delete_all', )],
                [('delete', '10.5.24.97')]
                [('edit', $old, $new)]
                [('add', {'name': 'test', 'ip_address_mask': ''})]
                action: add|delete|delete_all|edit|exist
                    add parameters:
                        dest_add_net: str
                        type: 'next_hop'|'interface'
                        next_hop: str
                        interface: 'WAN1'|'WAN2'|'Wi-Fi(STA)'| 'Cellular'
                        priority: int
                        description: str
                        save: True, False, dict
                        cancel: True, False, dict
                        text_messages: str or list
                        tip_messages: str or list
        :return:
        """
        self.access_menu('services')
        self.agg_in(FunctionsLocators(self.page, self.locale, self.model).static_routes,
                    {**{'expand': 'expand'}, **kwargs})


class DynamicDns(BasePage):
    @allure.step('配置Dynamic DNS')
    def config(self, **kwargs):
        """
        :param kwargs:
            dynamic_dns:
                [($action, **kwarg)] ex: [('delete_all', )],
                [('delete', '10.5.24.97')]
                [('edit', $old, $new)]
                [('add', {'name': 'test', 'ip_address_mask': ''})]
                action: add|delete|delete_all|edit|exist
                    add parameters:
                        service_provider: 'dyndns'|'3322'|'oray'|'no-ip'|'custom'
                        url_address: str
                        hostname: str
                        username: str
                        password: int
                        update_time: int
                        update_interface: 'WAN1'|'WAN2'|'Wi-Fi(STA)'| 'Cellular'
                        save: True, False, dict
                        cancel: True, False, dict
                        text_messages: str or list
                        tip_messages: str or list
        :return:
        """
        self.access_menu('services')
        self.agg_in(FunctionsLocators(self.page, self.locale, self.model).dynamic_dns,
                    {**{'expand': 'expand'}, **kwargs})


class PassthroughSettings(BasePage):
    @allure.step('配置passthrough settings')
    def config(self, **kwargs):
        """
        :param kwargs:
            ip_passthrough: 'enable'|'disable'
            passthrough_mac: str
            passthrough_wan: 'WAN1'|'WAN2'|'Wi-Fi(STA)'| 'Cellular'
            passthrough_lan: str
            dhcp_server: 'check'|'uncheck'
            lease: '1_day'|'1_hour'|'1_week'|'12_hours'|'6_hours'
            save: True, False, dict
            reset: True, False, dict
            text_messages: str or list
            tip_messages: str or list
        :return:
        """
        self.access_menu('services')
        self.agg_in(FunctionsLocators(self.page, self.locale, self.model).passthrough_settings,
                    {**{'expand': 'expand'}, **kwargs})


class CloudManagement(BasePage):

    @allure.step("编辑Cloud Management")
    def config(self, **kwargs):
        """
        :param kwargs:
            enabled_cloud_management: 'enable'|'disable'
            cloud_platform: 'incloud_manager_china'|'incloud_manager_global'
            mqtt_keepalive_time: str, 60-3600
            log_reporting: 'enable'|'disable'
            save: True, False, dict
            reset: True, False
            text_messages: str or list
            tip_messages: str or list
        """
        self.access_menu('system')
        self.agg_in(FunctionsLocators(self.page, self.locale, self.model).cloud_management,
                    {**{'cloud_management': 'expand'}, **kwargs})


class RemoteAccessControl(BasePage):
    @allure.step("编辑Remote Access Control")
    def config(self, **kwargs):
        """
        :param kwargs:
            enable_https: 'enable'|'disable'
            https_port: str, 1-65535
            enable_ssh: 'enable'|'disable'
            ssh_port: str, 1-65535
            enable_ping: 'enable'|'disable'
            save: True, False, dict
            reset: True, False
            text_messages: str or list
            tip_messages: str or list
        """
        self.access_menu('system')
        self.agg_in(FunctionsLocators(self.page, self.locale, self.model).remote_access_control,
                    {**{'remote_access_control': 'expand'}, **kwargs})


class SystemClock(BasePage):
    @allure.step("编辑System Clock")
    def config(self, **kwargs):
        """
        :param kwargs:
            time_zone: str, 'kwajalein'|'midway_island'|'hawaii'|...
            enable_ntp_server: 'enable'|'disable'
            ntp_server_1: str, 'pool.ntp.org'
            ntp_server_1_port: str, 1-65535
            ntp_server_2: str, 'pool.ntp.org'
            ntp_server_2_port: str, 1-65535
            save: True, False, dict
            reset: True, False
            text_messages: str or list
            tip_messages: str or list
        """
        self.access_menu('system')
        self.agg_in(FunctionsLocators(self.page, self.locale, self.model).system_clock,
                    {**{'system_clock': 'expand'}, **kwargs})


class DeviceOptions(BasePage):
    @allure.step("编辑Device Options")
    def config(self, **kwargs):
        """
        :param kwargs:
            reboot: True, False, dict {'dialog_message': $dialog_message, 'text_messages': $text_messages}
            ok: True, False, dict  重启的弹窗
            cancel: True, False, dict  重启的弹窗
            upgrade: dict, {'file_path': $file_path, 'dialog_message': $dialog_message, 'tip_message': tip_message}
            ok: True, False, dict  升级的弹窗
            cancel: True, False, dict  升级的弹窗
            restore_to_factory: True, False, dict {'dialog_message': $dialog_message, 'text_messages': $text_messages}
            ok: True, False, dict  恢复出厂设置的弹窗
            cancel: True, False, dict  恢复出厂设置的弹窗
            save: True, False, dict
            reset: True, False
            text_messages: str or list
            tip_messages: str or list
        """
        self.access_menu('system')
        self.agg_in(FunctionsLocators(self.page, self.locale, self.model).device_options,
                    {**{'device_options': 'expand'}, **kwargs})


class ConfigurationManagement(BasePage):
    @allure.step("编辑Configuration Management")
    def config(self, **kwargs):
        """
        :param kwargs:
            export: dict, {'file_path': $file_path, 'file_name': file_name}
            import: dict, {'file_path': $file_path, 'dialog_message': $dialog_message, 'tip_message': tip_message}
            ok: True, False, dict  导入配置文件的弹窗
            cancel: True, False, dict 导入配置文件的弹窗
            save: True, False, dict
            text_messages: str or list
            tip_messages: str or list
        """
        self.access_menu('system')
        self.agg_in(FunctionsLocators(self.page, self.locale, self.model).configuration_management,
                    {**{'configuration_management': 'expand'}, **kwargs})


class DeviceAlarms(BasePage):
    @allure.step("编辑Device Alarms")
    def config(self, **kwargs):
        """
        :param kwargs:
            # 以下为告警规则选择, 默认都不选, 需要则传入列表
            alarm_rule_select: str or list,默认都为不选, 需要则传入列表, 全选传 'select_all', 全不选传[]
                        'select_all'|['user_login_success',...,'cpu_too_high', 'memory_too_high',...]
                    'user_login_success'|'user_login_fail'|'configuration_change'|'cpu_too_high'|'cpu_height_setting'|
                    'memory_too_high'|'memory_height_setting'|'detection_status_change'|'vpn_status_change'|
                    'uplink_status_change'|'failover_occurs'|'reboot'|'upgrade'
            alarm_select_save: 保存告警规则选择, True, False, dict
            alarm_select_reset: True, False
            enable_receive_email_settings: 'enable'|'disable'
            mail_server_address: str, 发件服务器地址
            mail_server_port: str, 1-65535
            username: str, 用户名
            password: str, 密码
            tls: 'check'|'uncheck'
            receiving_email_address: str or list, 收件邮箱地址
            send_a_test_email_to: str, 发送测试邮件到，传了该参数时, 会默认发送测试邮件
            send: 发送按钮, True, False, dict
            text_messages: str or list
            tip_messages: str or list
        """
        self.access_menu('system')
        if 'send_a_test_email_to' in kwargs.keys() and kwargs.get('send_a_test_email_to'):
            kwargs.update({'send': True})
        if kwargs.get('alarm_rule_select') is not None:
            rules = kwargs.pop('alarm_rule_select')
            if isinstance(rules, str):
                kwargs.update({'select_all': 'check'})
            elif isinstance(rules, list):
                kwargs.update({'select_all': 'uncheck'})
                for rule in ['user_login_success', 'user_login_fail', 'configuration_change', 'cpu_too_high',
                             'cpu_height_setting', 'memory_too_high', 'memory_height_setting',
                             'detection_status_change',
                             'vpn_status_change', 'uplink_status_change', 'failover_occurs', 'reboot', 'upgrade']:
                    if rule in rules:
                        kwargs.update({rule: 'check'})
                    else:
                        kwargs.update({rule: 'uncheck'})
            else:
                raise TypeError('alarm_rule_select type error')
        self.agg_in(FunctionsLocators(self.page, self.locale, self.model).device_alarms,
                    {**{'device_alarms': {'wait_for_time': 1000}}, **kwargs})

    @allure.step("校验事件的邮件")
    def assert_event_mail(self, receiver: tuple, mail_from: tuple, event_type: str, imap_server='imap.exmail.qq.com',
                          **kwargs):
        """收取符合条件的邮件做校验，如果匹配到多个邮件，只校验最近的一封邮件
               当邮箱中邮件较多时，会耗时很长，所以建议匹配未读的邮件进行分析，分析完后，将邮件标记为已读

            :param receiver: 接收者('test@inhand.com.cn', '1111124') email, password
            :param mail_from: 发送者('映翰通网络', 'iot_console@inhand.com.cn') name, email
            :param imap_server: imap server地址
            :param event_type: 事件类型， test_email| login_success| login_fail| config_change| cell_type_threshold| detection_success|
                            detection_fail| wan1_connect| wan1_disconnect| wan1_to_sim1| sim1_to_wan1|
                            wan1_to_wan2| wan2_to_wan1| ipsec_connect| ipsec_disconnect| l2tp_connect|
                            l2tp_disconnect| wan2_to_lan1| lan1_to_wan2| reboot| upgrade
            :param kwargs:
                          timeout: 超时时间，单位秒
                          interval: 每隔多久检查一次，单位秒
            :return:
            """
        events_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
                                   'er_events.yaml')
        events_config = read_yaml_file(events_path).get(self.language).get(event_type)
        receive_last_mail(receiver, mail_from, events_config.get('type'), imap_server, assert_body=events_config.get('message'), **kwargs)


class Tools(BasePage):
    @allure.step("编辑Tools")
    def config(self, **kwargs):
        """
        :param kwargs:
            # ping
            ping_target: str, ip or domain name
            ping_interface: str, 'Any'|'WAN1'|'WAN2'|'Cellular'|'WI-Fi(STA)'|'Default'
            ping_source: str,
            paket_size: str, 1 - 65535
            paket_number: str, 1 - 1000
            start_ping: True, False, dict
            stop_ping: True, False, dict
            clear_ping: True, False, dict
            # traceroute
            traceroute_target: str, ip or domain name
            traceroute_interface: str, 'Any'|'WAN1'|'WAN2'|'Cellular'|'WI-Fi(STA)'|'Default'
            start_traceroute: True, False, dict
            stop_traceroute: True, False, dict
            # capture
            capture_interface: str, 'Any'|'WAN1'|'WAN2'|'Cellular'|'WI-Fi(STA)'|'Default'
            filter_expression: str
            capture_time: str, 10-600
            capture_output: str, 'view_output_below'|'export'
            start_capture: True, False, dict
            stop_capture: True, False, dict
            clear_capture: clear_capture
            # iperf
            iperf_role: str, 角色 'server'|'client'
            iperf_time: str, 60-600
            start_iperf: True, False, dict
            stop_iperf: True, False, dict
            clear_iperf: True, False, dict
            text_messages: str or list
            tip_messages: str or list
        """
        self.access_menu('system')
        self.agg_in(FunctionsLocators(self.page, self.locale, self.model).tools,
                    {**{'tools': {'wait_for_time': 1000}}, **kwargs})


class ScheduledReboot(BasePage):
    @allure.step("编辑Scheduled Reboot")
    def config(self, **kwargs):
        """
        :param kwargs:
            scheduled_reboot_type: str,  'daily'|'weekly'|'monthly'|'never'
            start_time: str, 00:00-23:59|'now'
            weekday: 默认为都不选，需要选择传入列表, 不需要则不传, ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
            reboot_date: str, 1-31
            save: True, False, dict
            reset: True, False
            text_messages: str or list
            tip_messages: str or list
        """
        self.access_menu('system')
        if kwargs.get('weekday') is not None:
            week = kwargs.pop('weekday')
            for day in ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']:
                if day in week:
                    kwargs.update({day: 'check'})
                else:
                    kwargs.update({day: 'uncheck'})
        if 'start_time' in kwargs.keys() and kwargs.get('start_time'):
            kwargs.update({'start_time_click': True})
            if kwargs.get('start_time') == 'now':
                kwargs.pop('start_time')
                kwargs.update({'now': True})
            else:
                kwargs.update({'ok': True})
        self.agg_in(FunctionsLocators(self.page, self.locale, self.model).scheduled_reboot,
                    {**{'scheduled_reboot': 'expand'}, **kwargs})


class LogServer(BasePage):
    @allure.step("编辑Log Server")
    def config(self, **kwargs):
        """
        :param kwargs:
            enable_log_server: 'enable'|'disable'
            server_address1: str, ip or domain name
            port1: str, 1-65535
            server_address2: str, ip or domain name
            port2: str, 1-65535
            save: True, False, dict
            reset: True, False
            text_messages: str or list
            tip_messages: str or list
        """
        self.access_menu('system')
        self.agg_in(FunctionsLocators(self.page, self.locale, self.model).log_server,
                    {**{'log_server': 'expand'}, **kwargs})


class AccountManagement(BasePage):
    @allure.story('编辑Account Management')
    def config(self, **kwargs):
        """
        :param kwargs:
            username: str, 用户名
            password: str, 密码, 必填
            confirm_password: str, 确认密码, 必填
            save: True, False, dict
            reset: True, False
            text_messages: str or list
            tip_messages: str or list
        :return:
        """
        self.access_menu('system')
        self.agg_in(FunctionsLocators(self.page, self.locale, self.model).account_management,
                    {**{'account_management': 'expand'}, **kwargs})


class OtherSettings(BasePage):
    @allure.story('编辑Other Settings')
    def config(self, **kwargs):
        """
        :param kwargs:
            logout_timeout: str, 6-300, 登出时间
            logout_timeout_save: 保存登出时间配置 True, False, dict
            logout_timeout_reset: 重置 True, False
            accelerated_forwarding: 快速转发, 'enable'|'disable'
            accelerated_forwarding_save: 保存快速转发配置 True, False, dict
            accelerated_forwarding_reset: 重置 True, False
            automatically_restarts: 自动重启, 'enable'|'disable'
            automatically_restarts_save: 保存自动重启配置 True, False, dict
            automatically_restarts_reset: 重置 True, False
            sip_alg: 'enable'|'disable'
            sip_alg_save: 保存sip_alg配置 True, False, dict
            sip_alg_reset: 重置 True, False
            text_messages: str or list
            tip_messages: str or list
        :return:
        """
        self.access_menu('system')
        self.agg_in(FunctionsLocators(self.page, self.locale, self.model).other_settings,
                    {**{'other_settings': 'expand'}, **kwargs})


class Ssids(BasePage):
    @allure.step('配置wifi ssids')
    def config(self, **kwargs):
        """
        :param kwargs:
           band_24g:
                [($action, **kwarg)] ex: [('delete', $ssid)]
                [('delete', re.compile(r'test_24g_1.*2\.4Ghz')]
                [('edit', $old, $new)]   old有多个时， 默认对第一个做操作
                [('add', {'ssid': 'test_24g_1', 'ip_address_mask': ''})]
                [('edit', 'Default', {'permit': True})]默认规则编辑
                action: add|delete|delete_all|edit|exists
                    add sub wifi parameters: # 子wifi与主wifi信道一致, 无需配置
                        ssid: str
                        status: 'enable'|'disable'
                        security: 'wpa'|'wpa2'|'wpa-psk'|'wpa2-psk'|'wpa-psk/wpa2-psk'|'open'
                        encryption: 'ccmp'|'ccmp/tkip'
                        password: str,
                        network: 'default'|...
                        user_isolation: 'check'|'uncheck'
                        hide_ssid: 'check'|'uncheck'
                        save: True, False
                        cancel: True, False
                        text_messages: str or list
                        tip_messages: str or list
                edit parameters:
                    其余同上 add parameters
                    channel: str, 'auto'|'1'|'2'|'3'|'4'|'5'|'6'|'7'|'8'|'9'|'10'|'11'|'36'|'40'|'44'|'48'|'149'|'153'|'157'|'161'
                    bandwidth: str, '20'|'40'|'80'
           band_5g:
                 同上
        :return:
        """
        if self.model != 'EAP600':
            self.access_menu('wifi.ssids')
            for band_ in ['band_24g', 'band_5g']:
                for item in kwargs.get(band_, []):
                    if item[0] == 'add':
                        item[1].update({band_: 'check'})
            self.agg_in(FunctionsLocators(self.page, self.locale, self.model).ssids,
                        {'ssids': kwargs.get('band_24g', []) + kwargs.get('band_5g', [])})
        else:
            if kwargs.get('band_24g'):
                self.access_menu('wifi.ssid_24g')
                self.agg_in(FunctionsLocators(self.page, self.locale, self.model).ssids,
                            {'ssids': kwargs.get('band_24g')})
            if kwargs.get('band_5g'):
                self.access_menu('wifi.ssid_5g')
                self.agg_in(FunctionsLocators(self.page, self.locale, self.model).ssids,
                            {'ssids': kwargs.get('band_5g')})


class Portal(BasePage):

    @allure.step("编辑portal")
    def config(self, **kwargs):
        """
        :param kwargs:
            portal:
                [($action, **kwarg)] ex: [('delete_all', )],
                [('delete', 'aaaaa')]
                [('edit', $old, $new)]
                [('add', {'name': 'aaaaa', 'authentication_type': 'click_passthrough'})]
                action: add|delete|delete_all|edit|exist
                    add parameters:
                        name: str
                        authentication_type: 'click_passthrough'|'user_authentication'
                        target_ssid: list or str, 目标ssid, 多项选择
                        background_image: 'none'|'custom', 自定义时在参数background_image_choose_file中传入图片路径
                        background_image_choose_file: dict, 图片路径, {'file_path': $file_path, 'dialog_message': XX,...}
                        logo: 'none'|'custom', 自定义时在参数logo_choose_file中传入图片路径
                        logo_choose_file: dict, 图片路径, {'file_path': $file_path, 'dialog_message': XX,...}
                        splash_language: 'english'|'chinese'|'en'|'cn'
                        background_color: str, 'e9eaeb'|'202638'|...
                        title_color: str, 'e9eaeb'|'202638'|...
                        text_color: str, 'e9eaeb'|'202638'|...
                        box_color: str, 'e9eaeb'|'202638'|...
                        button_color: str, 'e9eaeb'|'202638'|...
                        title: str, 标题
                        welcome_message: str, 欢迎文本
                        button_text: str, 按钮文字
                        box_opacity: str, 0-100
                        next_behavior: str, 后续行为, 'stay_on_the_splash_page'|'redirect_url'
                        save: True, False, dict
                        cancel: True, False, dict
                        text_messages: str or list
                        tip_messages: str or list
        :return:
        """
        self.access_menu('wifi.portal')
        for key in ['background_color', 'title_color', 'text_color', 'box_color', 'button_color']:
            if kwargs.get(key):
                kwargs.update({key: True, f'{key}_input': kwargs.pop(key), f'{key}_confirm': True})
        self.agg_in(FunctionsLocators(self.page, self.locale, self.model).ipsec_vpn, kwargs)


class Wan(BasePage):
    @allure.step('配置wan')
    def config(self, **kwargs):
        """
        :param kwargs:
            type_: 'static_ip'|'dhcp'
            ip_address: str
            mask: str
            gateway_address: str
            main_dns: str
            secondary_dns: str
            mtu: str, 128-1500
            save: True, False, dict
            cancel: True, False, dict
            text_messages: str or list
            tip_messages: str or list
        :return:
        """
        self.access_menu('config.wan')
        self.agg_in(FunctionsLocators(self.page, self.locale, self.model).wan, kwargs)


class Radio(BasePage):
    @allure.step('配置radio')
    def config(self, **kwargs):
        """

        :param kwargs:
                24g_radio_channel_width: '20'|'40'
                24g_radio_transmit_power: 'auto'|'height'|'medium'|'low'|'custom.19' custom时，有效数值为1-20
                5g_radio_channel_width: '20'|'40'|'80'
                5g_radio_transmit_power: 'auto'|'height'|'medium'|'low'|'custom.19' custom时，有效数值为1-20
                wireless_mesh: 'enable'|'disable'
                save: True, False, dict
                reset: True, False, dict
                text_messages: str or list
                tip_messages: str or list

        :return:
        """
        self.access_menu('config.radio')
        for key, value in kwargs.items():
            if 'channel_width' in key and value:
                kwargs.update({f'{key}_{value}': True})
                kwargs.pop(key)
            elif 'transmit_power' in key and value:
                if 'custom' in value:
                    kwargs.update({key: 'custom', f'{key}_custom': value.split('.')[1]})
        self.agg_in(FunctionsLocators(self.page, self.locale, self.model).radio, kwargs)


class Dashboard(BasePage):

    @allure.step('断言设备信息')
    @loop_inspector('device_information')
    def assert_device_information(self, **kwargs):
        """
        :param kwargs: {$key: $expect_value}
                    key: name|model|serial|firmware_version|mac|uptime|internet_access|
                         uplink_ip|local_gateway_ip|system_time|license_status|
                    expect_value: 完整表达式, 当判断int型的关系时${value}和期望值可加"",而当需要调用str型的关系时${value}和期望值都要加"",
                         例:（'${value}==1', '${value}!=1', '${value}>1', '${value}>=1', '${value}<1', '${value}<=1', "${value}"=="abc"
                        '"${value}".startswith("123")', '"${value}".endswith("23")', '"${value}" in a', '"${value}" not in b',
                        '"${value}".__contains__("234")', 'time.strptime("${value}}", "%Y-%m-%d %H:%M:%S")'）
                    e.g {'name': "'${value}'.upper() == 'ER2000'", 'model': '"LITE" in "${value}"', ...}


        """
        self.access_menu('dashboard')
        locators = FunctionsLocators(self.page, self.locale, self.model).device_information
        return self.eval_locator_attribute(kwargs, locators)

    @allure.step('获取设备信息')
    def get_device_information(self, keys: str or list or tuple) -> str or dict or None:
        """

        :param keys: str or list or tuple , value
                        name|model|serial|firmware_version|mac|uptime|internet_access|
                         uplink_ip|local_gateway_ip|system_time|license_status|
                    e.g 'name' or ['name', 'model'] or ('name', 'serial')
        :return: value or {'name': 'ER805'}
        """

        if keys:
            self.access_menu('dashboard')
            locators = FunctionsLocators(self.page, self.locale, self.model).device_information
            return self.get_text(keys, locators)

    @allure.step('断言接口状态')
    @loop_inspector('interface_status')
    def assert_interface_status(self, **kwargs):
        """
        :param kwargs: 'lan1'|'lan2'|'lan3'|'lan4'|'lan5'|'wan1'|'wan2'|'cellular'|'wifi_sta'
            lan1: dict, key: status|link_rate|network
                            e.g. {'status': "'${value}'=='connected'", 'link_rate': '"100Mbps" in "${value}"', ...}
            lan2: 同lan1
            lan3: 同lan1
            lan4: 同lan1
            lan5: 同lan1
            wan1: dict, key: status|work_mode|ipv4_type|ipv4_address|ipv4_gateway|lease_acquisition_time|lease_timeout|
                             primary_dns|secondary_dns|ipv6_type|ipv6_address|ipv6_gateway|main_ipv6_dns|
                             secondary_ipv6_dns|test_connectivity_to
            wan2: 同wan1
            cellular: dict, key: status|work_mode|sim|carrier|network_mode|apn|ipv4_address|ipv4_gateway|primary_dns|
                                 secondary_dns|ipv6_address|ipv6_gateway|test_connectivity_to|used_traffic_threshold|
                                 iccid|imei|imsi|pci|cell_id|lac|arfcn|band|traffic_reset_time|connect_time
            wifi_sta: dict, key: status|work_mode|ssid|band|type|ip_address|gateway_address|lease_acquisition_time|
                                 lease_timeout|primary_dns|secondary_dns|test_connectivity_to|connect_time
        """
        self.access_menu('dashboard')
        locators = FunctionsLocators(self.page, self.locale, self.model).interface_status
        for param, value in kwargs.items():
            new_kwarg = {}
            if not self.page.locator('.anticon.anticon-close').is_visible():
                self.agg_in(FunctionsLocators(self.page, self.locale, self.model).interface_status, {param: True})
            else:
                self.agg_in(FunctionsLocators(self.page, self.locale, self.model).interface_status,
                            {f'{param}_expand': 'expand'})
            for key, value_ in value.items():
                new_kwarg.update({f'{param}_{key}': value_})
            result = self.eval_locator_attribute(new_kwarg, locators)
            if not result:
                self.agg_in(FunctionsLocators(self.page, self.locale, self.model).interface_status, {'close': True})
                return False
        else:
            self.agg_in(FunctionsLocators(self.page, self.locale, self.model).interface_status, {'close': True})
            return True

    @allure.step('获取接口状态')
    def get_interface_status(self, keys: str or list or tuple) -> str or dict or None:
        """

        :param keys: str or list or tuple , value
                        lan1_status|lan1_link_rate|lan1_network|lan2_status|lan2_link_rate|...|
                        wan1_status|wan1_work_mode|wan1_ipv4_type|wan1_ipv4_address|wan1_ipv4_gateway|
                        wan1_lease_acquisition_time|wan1_lease_timeout|wan1_primary_dns|wan1_secondary_dns|
                        wan1_ipv6_type|wan1_ipv6_address|wan1_ipv6_gateway|wan1_main_ipv6_dns|
                        wan1_secondary_ipv6_dns|wan1_test_connectivity_to|wan2_status|...|
                        cellular_status|cellular_work_mode|cellular_sim|cellular_carrier|cellular_network_mode|
                        cellular_apn|cellular_ipv4_address|cellular_ipv4_gateway|cellular_primary_dns|
                        cellular_secondary_dns|cellular_ipv6_address|cellular_ipv6_gateway|
                        cellular_test_connectivity_to|cellular_used_traffic_threshold|cellular_iccid|cellular_imei|
                        cellular_imsi|cellular_pci|cellular_cell_id|cellular_lac|cellular_arfcn|cellular_band|
                        cellular_traffic_reset_time|cellular_connect_time
                        wifi_sta_status|wifi_sta_work_mode|wifi_sta_ssid|wifi_sta_band|wifi_sta_type|
                        wifi_sta_ip_address|wifi_sta_gateway_address|wifi_sta_lease_acquisition_time|
                        wifi_sta_lease_timeout|wifi_sta_primary_dns|wifi_sta_secondary_dns|
                        wifi_sta_test_connectivity_to|wifi_sta_connect_time
                    e.g 'lan1_status', ['wan1_status', 'wifi_sta_status'], ('wan1_status', 'wifi_sta_status')
        :return: value or {'name1': value}
        """

        if keys:
            self.access_menu('dashboard')
            locators = FunctionsLocators(self.page, self.locale, self.model).interface_status
            keys, result = list(keys), {}
            for iface in ['lan1', 'lan2', 'lan3', 'lan4', 'lan5', 'wan1', 'wan2', 'cellular', 'wifi_sta']:
                sub_keys = list(filter(lambda x: iface in x, keys))
                if len(sub_keys):
                    self.agg_in(FunctionsLocators(self.page, self.locale, self.model).interface_status, {iface: True})
                    if len(sub_keys) == 1:
                        result.update({sub_keys[0]: self.get_text(sub_keys, locators)})
                    else:
                        result.update(self.get_text(sub_keys, locators))
                    self.agg_in(FunctionsLocators(self.page, self.locale, self.model).interface_status, {'close': True})
            return result

    @allure.step('获取流量统计')
    def get_data_usage_by_api(self) -> dict:
        """ 获取流量统计的信息

        :return:
        """
        return self.api.get_status('date_usage')

    @allure.step('获取 wi-fi 连接信息')
    def get_wlan_ap_by_api(self) -> dict:
        """ 获取wi-fi 连接的信息

        :return:
        """
        return self.api.get_status('wlan_ap')

    @allure.step('断言客户端流量top5')
    def assert_client_top5(self, top: dict):
        """判断是否存在client

        :param top: {"Default": {"connection": "Default", 'ip': "192.168.3.100", 'mac': "00:0e:c6:31:bf:a1",
                         'name': "00:0e:c6:31:bf:a1", 'rx': 34498, 'tx': 31077, 'type': "wired", 'uptime': 87500,
                         'vlan': 1}} 不需要的字段可以不传
        :return:
        """
        device_path = "{}://{}".format(self.protocol, self.host)
        with self.page.expect_response(
                lambda response: f"{device_path}/api/v1/status/clients" == response.url) as response_info:
            self.access_menu('dashboard')
        self.page.locator('.echarts-for-react ').last.is_visible()
        clients = response_info.value.json().get('result').get('clients')
        for key, value in top.items():
            for client in clients:
                if key == client.get('connection'):
                    for parameter in ('connection', 'ip', 'mac', 'name', 'type', 'vlan'):
                        if parameter in value.keys():
                            assert value.get(parameter) == client.get(
                                parameter), f"the expect is {value}, now is {client}"
                    if 'uptime' in value.keys():
                        assert client.get('uptime') - value.get('uptime') <= 50
                    if 'rx' in value.keys():
                        assert client.get('rx') >= value.get('rx'), f"the expect is {value}, now is {client}, rx error"
                    if 'tx' in value.keys():
                        assert client.get('tx') >= value.get('tx'), f"the expect is {value}, now is {client} tx error"
                    break
            else:
                raise Exception(f'not found this client {key}')

    @allure.step('断言流量统计')
    def assert_traffic_statistics(self):
        """校验流量统计

        :return:
        """
        device_path = "{}://{}".format(self.protocol, self.host)
        with self.page.expect_response(
                lambda response: f"{device_path}/api/v1/status/data_usage" == response.url) as response_info:
            self.access_menu('dashboard')
        self.page.locator('.echarts-for-react ').last.is_visible()
        interface_name_list = response_info.value.json().get('result').get('data_usage')
        assert self.page.locator(
            f'//div[./div[text()="{self.locale.get("traffic_statistics")}"]]').locator(
            '//div[@class="echarts-for-react "]').count() == 1, 'assert traffic statistic error'
        for i in interface_name_list:
            assert i.get('tx') != 0, f'assert {i.get("name")}\'s tx traffic error'
            assert i.get('rx') != 0, f'assert {i.get("name")}\'s rx traffic error'
