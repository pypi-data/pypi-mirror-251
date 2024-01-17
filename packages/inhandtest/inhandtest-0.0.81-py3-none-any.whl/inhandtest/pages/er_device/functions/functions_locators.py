# -*- coding: utf-8 -*-
# @Time    : 2023/11/30 16:18:19
# @Author  : Pane Li
# @File    : functions_locators.py
"""
functions_locators

"""
import dynaconf
from playwright.sync_api import Page
from inhandtest.pages.adapt_model_locator import AdaptModelLocator


class FunctionsLocators(AdaptModelLocator):

    def __init__(self, page: Page, locale: dynaconf.base.LazySettings, model: str):
        super().__init__(model)
        self.page = page
        self.locale = locale
        self.pop_up = self.page.locator('.ant-modal-content')

    @property
    @AdaptModelLocator.adapt_model
    def lan_or_localnetwork(self) -> list:
        return [
            ('lan_resource',
             {'table': [
                 ('add', {'locator': {'default': self.page.locator('.anticon.anticon-plus').first}, 'type': 'button'}),
                 ('name', {'locator': {'default': self.page.locator('#lan_modal_alias')}, 'type': 'fill'}),
                 ('mode', {'locator': {
                     'default': self.page.locator('#lan_modal_l3_vlan')}, 'type': 'radio_select',
                     'param': {'ip_mode': self.locale.ip_mode, 'vlan_only_mode': self.locale.vlan_only_mode}}),
                 ('type', {'locator': {
                     'default': self.page.locator('#lan_modal_guest')}, 'type': 'radio_select',
                     'param': {'standrad': self.locale.standard, 'guest': self.locale.guest}}),
                 ('vlan', {'locator': {'default': self.page.locator('#lan_modal_vlan')}, 'type': 'fill'}),
                 ('ip_address_mask', {'locator': {'default': self.page.locator('#lan_modal_ipv4_ip')},
                                      'type': 'fill', "relation": [('mode', 'ip_mode')]}),
                 ('ip_address', {'locator': {'default': self.pop_up.locator(
                     '//div[@class="ant-space ant-space-horizontal ant-space-align-center"]').locator(
                     '//input[@type="text"]').first, }, 'type': 'fill', "relation": [('mode', 'ip_mode')]}),
                 ('mask', {'locator': {'default': self.pop_up.locator(
                     '//div[@class="ant-space ant-space-horizontal ant-space-align-center"]').locator(
                     '//input[@class="ant-input-number-input"]').first}, 'type': 'fill',
                           "relation": [('mode', 'ip_mode')]}),
                 ('dhcp_server', {'locator': {'default': self.page.locator('#lan_modal_enabled')},
                                  'type': 'switch_button', "relation": [('mode', 'ip_mode')]}),
                 ('dhcp_ip_range_start_ip', {'locator': {'default': self.page.locator('#lan_modal_ip_pool_start_ip')},
                                             'type': 'fill', "relation": [('mode', 'ip_mode')]}),
                 ('dhcp_ip_range_end_ip', {'locator': {'default': self.page.locator('#lan_modal_ip_pool_end_ip')},
                                           'type': 'fill', "relation": [('mode', 'ip_mode')]}),
                 ('ipv6', {'locator': {'default': self.page.locator('#lan_modal_ipv6_mode')}, 'type': 'select',
                           'param': {'disable': self.locale.disable, 'auto': self.locale.auto,
                                     'static_ip': self.locale.static_ip}}),
                 ('ipv6_address', {'locator': {'default': self.pop_up.locator(
                     '//div[@class="ant-space ant-space-horizontal ant-space-align-center"]').locator(
                     '//input[@type="text"]').last}, 'type': 'fill', 'relation': [('ipv6', 'static_ip')]}),
                 ('ipv6_prefix_length', {'locator': {'default': self.pop_up.locator(
                     '//div[@class="ant-space ant-space-horizontal ant-space-align-center"]').locator(
                     '//input[@class="ant-input-number-input"]').last}, 'type': 'fill',
                                         'relation': [('ipv6', 'static_ip')]}),
                 ('save', {'locator': {'default': self.page.locator(
                     '//button[@class="ant-btn ant-btn-primary"]')}, 'type': 'button',
                     'wait_for': {'type': 'hidden', 'locator': self.pop_up, 'timeout': 300 * 1000}}),
                 ('text_messages', {'type': 'text_messages'}),
                 ('tip_messages', {'type': 'tip_messages'}),
                 ('cancel',
                  {'locator': self.page.locator('//button[@class="ant-btn ant-btn-default"]'), 'type': 'button',
                   "always_do": True}),
                 ('pop_up', {'locator': {'default': self.pop_up}, 'type': 'button'}),
                 ('action_confirm', {'locator': {'default': self.page.locator('.ant-popover-inner-content').locator(
                     '.ant-btn.ant-btn-primary.ant-btn-sm.ant-btn-dangerous').first}, 'type': 'button'})],
                 'locator': {'default': self.page.locator('.ant-table-container').nth(0)}, 'type': 'table_tr', })
        ]

    @property
    @AdaptModelLocator.adapt_model
    def wan(self) -> list:
        return [
            ('type', {'locator': {'default': self.page.locator('#ipType'),
                                  'EAP600': self.page.locator('#ipType')}, 'type': 'select'}),
            ('ip_address', {'locator': {'default': self.page.locator('#ip'),
                                        'EAP600': self.page.locator('#ip')}, 'type': 'fill'}),
            ('mask', {'locator': {'default': self.page.locator('#mask'),
                                  'EAP600': self.page.locator('#mask')}, 'type': 'fill'}),
            ('gateway_address', {'locator': {"default": self.page.locator('#gateway'),
                                             "EAP600": self.page.locator('#gateway')}, 'type': 'input'}),
            ('main_dns', {'locator': {"default": self.page.locator('#dns1'),
                                      'EAP600': self.page.locator('#dns1')}, 'type': 'fill', }),
            ('secondary_dns', {'locator': {"default": self.page.locator('#dns2'),
                                           'EAP600': self.page.locator('#dns2')}, 'type': 'fill'}),
            ('mtu', {'locator': {"default": self.page.locator('#mtu'),
                                 'EAP600': self.page.locator('#mtu')}, 'type': 'fill'}),
            ('save', {'locator': {"default": self.page.locator(f'button:has-text("{self.locale.get("save")}")'),
                                  'EAP600': self.page.locator(f'button:has-text("{self.locale.get("save")}")')},
                      'type': 'button'}),
            ('reset', {'locator': {"default": self.page.locator(f'button:has-text("{self.locale.get("reset")}")'),
                                   'EAP600': self.page.locator(f'button:has-text("{self.locale.get("reset")}")')},
                       'type': 'button'}),
        ]

    @property
    @AdaptModelLocator.adapt_model
    def internet(self) -> list:
        return [
            ('uplink_table',
             {'table': [
                 ('add', {'locator': {'default': self.page.locator('.anticon.anticon-plus').first}, 'type': 'button'}),
                 ('name', {'locator': {'default': self.page.locator('#name')}, 'type': 'radio_select'}),
                 ('status', {'locator': {'default': self.page.locator('#status')}, 'type': 'switch_button'}),
                 ('nat', {'locator': {'default': self.page.locator('#nat')}, 'type': 'check'}),
                 ('ipv4_type', {'locator': {'default': self.page.locator('#ipType')}, 'type': 'select',
                                'param': {'dhcp': 'DHCP', 'static_ip': self.locale.static_ip, 'pppoe': 'PPPoE'}}),
                 ('ipv4_address', {'locator': {'default': self.page.locator('#ip')}, 'type': 'fill'}),
                 ('mask', {'locator': {'default': self.page.locator('#mask')}, 'type': 'fill'}),
                 ('ipv4_gateway_address', {'locator': {'default': self.page.locator('#gateway')}, 'type': 'fill'}),
                 ('main_dns', {'locator': {'default': self.page.locator('#dns1')}, 'type': 'fill'}),
                 ('secondary_dns', {'locator': {'default': self.page.locator('#dns2')}, 'type': 'fill'}),
                 ('pppoe_user_name', {'locator': {'default': self.page.locator('#pppoe_username')}, 'type': 'fill'}),
                 ('pppoe_password', {'locator': {'default': self.page.locator('#pppoe_password')}, 'type': 'fill'}),
                 ('local_ip_address', {'locator': {'default': self.page.locator('#pppoe_local_ip')}, 'type': 'fill'}),
                 ('remote_ip_address', {'locator': {'default': self.page.locator('#pppoe_remote_ip')}, 'type': 'fill'}),
                 ('ipv6_type', {'locator': {'default': self.page.locator('#ipv6_mode')}, 'type': 'select',
                                'param': {'disable': self.locale.disable, 'static_ip': self.locale.static_ip,
                                          'auto': self.locale.auto}}),
                 ('ipv6_address', {'locator': {'default': self.page.locator('#ipv6_ip')}, 'type': 'fill'}),
                 ('prefix_length', {'locator': {'default': self.page.locator('#ipv6_prefix_len')}, 'type': 'fill'}),
                 ('ipv6_gateway_address', {'locator': {'default': self.page.locator('#ipv6_gateway')}, 'type': 'fill'}),
                 ('main_ipv6_dns', {'locator': {'default': self.page.locator('#ipv6_dns1')}, 'type': 'fill'}),
                 ('secondary_ipv6_dns', {'locator': {'default': self.page.locator('#ipv6_dns2')}, 'type': 'fill'}),
                 ('mtu', {'locator': {'default': self.page.locator('#mtu')}, 'type': 'fill'}),
                 ('band', {'locator': {'default': self.page.locator('#band')}, 'type': 'radio_select',
                           'param': {'2.4g': '2.4GHz', '5g': '5GHz'}}),
                 ('ssid', {'locator': {'default': self.page.locator('#ssid')}, 'type': 'fill'}),
                 ('security', {'locator': {'default': self.page.locator('#auth')}, 'type': 'select',
                               'param': {'open': 'OPEN', 'wpa_psk': 'WPA-PSK',
                                         'wpa2_psk': 'WPA2-PSK', 'wpa_wpa2_psk': 'WPA-PSK/WPA2-PSK'}}),
                 ('encryption', {'locator': {'default': self.page.locator('#encrypt')}, 'type': 'select',
                                 'param': {'ccmp': 'CCMP', 'ccmp_tkip': 'CCMP/TKIP'}}),
                 ('wlan_password', {'locator': {'default': self.page.locator('#key')}, 'type': 'fill'}),
                 ('work_mode', {'locator': {'default': self.page.locator('#simMode')}, 'type': 'select',
                                'param': {'only_sim1': self.locale.only_sim1, 'only_sim2': self.locale.only_sim2,
                                          'dual_mode': self.locale.dual_mode}}),
                 ('primary_card', {'locator': {'default': self.page.locator('#mainSim')}, 'type': 'select',
                                   'param': {'sim1': 'SIM1', 'sim2': 'SIM2'},
                                   'relation': [('work_mode', 'dual_mode')]}),
                 ('sim1_tab', {'locator': {'default': self.page.locator('.ant-tabs-tab-btn').nth(0)}, 'type': 'click'}),
                 ('sim1_dialing_parameters',
                  {'locator': {'default': self.page.locator('#sim1_dialingParameters')}, 'type': 'select',
                   'param': {'auto': self.locale.auto, 'manual': self.locale.manual}}),
                 (
                     'sim1_service_type',
                     {'locator': {'default': self.page.locator('#sim1_network_type')}, 'type': 'select',
                      'param': {'auto': self.locale.auto, '2g': '2G', '3g': '3G', '4g': '4G',
                                '5g_sa': '5G SA', '4g&5g': '4G&5G'}}),
                 ('sim1_5g_type', {'locator': {'default': self.page.locator('#sim1_nr5g_mode')}, 'type': 'select',
                                   'param': {'sa': 'SA', 'nsa': 'NSA', 'sa_nsa': 'SA/NSA', 'sa_nsa_lte': 'SA/NSA/LTE',
                                             'nsa_lte': 'NSA/LTE', 'sa_lte': 'SA/LTE'}}),
                 ('sim1_pin_code', {'locator': {'default': self.page.locator('#sim1_pin_code')}, 'type': 'fill'}),
                 ('sim1_ims', {'locator': {'default': self.page.locator('#sim1_ims')}, 'type': 'select',
                               'param': {'auto': self.locale.auto, 'enable': self.locale.enable,
                                         'disable': self.locale.disable}}),
                 ('sim1_ip_type', {'locator': {'default': self.page.locator('#sim1_type')}, 'type': 'select',
                                   'param': {'ipv4': 'IPv4', 'ipv6': 'IPv6', 'ipv4&ipv6': 'IPv4&IPv6'}}),
                 ('sim1_apn', {'locator': {'default': self.page.locator('#sim1_apn')}, 'type': 'fill'}),
                 ('sim1_authentication', {'locator': {'default': self.page.locator('#sim1_auth')}, 'type': 'select',
                                          'param': {'auto': self.locale.auto, 'pap': 'PAP', 'chap': 'CHAP',
                                                    'ms_chap': 'MS-CHAP',
                                                    'ms_chapv2': 'MS-CHAPv2'}}),
                 ('sim1_username', {'locator': {'default': self.page.locator('#sim1_username')}, 'type': 'fill'}),
                 ('sim1_password', {'locator': {'default': self.page.locator('#sim1_password')}, 'type': 'fill'}),
                 ('sim2_tab', {'locator': {'default': self.page.locator('.ant-tabs-tab-btn').nth(1)}, 'type': 'click'}),
                 ('sim2_dialing_parameters',
                  {'locator': {'default': self.page.locator('#sim2_dialingParameters')}, 'type': 'select',
                   'param': {'auto': self.locale.auto, 'manual': self.locale.manual}}),
                 (
                     'sim2_service_type',
                     {'locator': {'default': self.page.locator('#sim2_network_type')}, 'type': 'select',
                      'param': {'auto': self.locale.auto, '2g': '2G', '3g': '3G', '4g': '5G',
                                '5g_sa': '5G SA', '4g&5g': '4G&5G'}}),
                 ('sim2_5g_type', {'locator': {'default': self.page.locator('#sim2_nr5g_mode')}, 'type': 'select',
                                   'param': {'auto': self.locale.auto, '2g': '2G', '3g': '3G', '4g': '5G',
                                             'sa': 'SA', 'nsa': 'NSA', 'sa_nsa': 'SA/NSA'}}),
                 ('sim2_pin_code', {'locator': {'default': self.page.locator('#sim2_pin_code')}, 'type': 'fill'}),
                 ('sim2_ims', {'locator': {'default': self.page.locator('#sim2_ims')}, 'type': 'select',
                               'param': {'auto': self.locale.auto, 'enable': self.locale.enable,
                                         'disable': self.locale.disable}}),
                 ('sim2_ip_type', {'locator': {'default': self.page.locator('#sim2_type')}, 'type': 'select',
                                   'param': {'ipv4': 'IPv4', 'ipv6': 'IPv6', 'ipv4&ipv6': 'IPv4&IPv6'}}),
                 ('sim2_apn', {'locator': {'default': self.page.locator('#sim2_apn')}, 'type': 'fill'}),
                 ('sim2_authentication', {'locator': {'default': self.page.locator('#sim2_auth')}, 'type': 'select',
                                          'param': {'auto': self.locale.auto, 'pap': 'PAP', 'chap': 'CHAP',
                                                    'ms_chap': 'MS-CHAP',
                                                    'ms_chapv2': 'MS-CHAPv2'}}),
                 ('sim2_username', {'locator': {'default': self.page.locator('#sim2_username')}, 'type': 'fill'}),
                 ('sim2_password', {'locator': {'default': self.page.locator('#sim2_password')}, 'type': 'fill'}),
                 ('cellular_mtu_mode', {'locator': {'default': self.pop_up.locator(
                     '//div[@class="ant-space ant-space-horizontal ant-space-align-center"]').locator(
                     '//input[@class="ant-select-selection-search-input"]')}, 'type': 'select',
                     'param': {'auto': self.locale.auto, 'manual': self.locale.manual}}),
                 ('cellular_mtu_input', {'locator': {'default': self.pop_up.locator(
                     '//div[@class="ant-space ant-space-horizontal ant-space-align-center"]').locator(
                     "//input[@class='ant-input-number-input']")},
                     'type': 'fill', 'relation': [('cellular_mtu_mode', 'manual')]}),
                 ('save', {'locator': self.pop_up.locator(
                     '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button',
                     'wait_for': {'type': 'hidden', 'locator': self.pop_up, 'timeout': 300 * 1000}}),
                 ('text_messages', {'type': 'text_messages'}),
                 ('tip_messages', {'type': 'tip_messages'}),
                 ('cancel',
                  {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-default"]'), 'type': 'button',
                   "always_do": True}),
                 ('pop_up', {'locator': {'default': self.pop_up, 'default': self.pop_up}, 'type': 'button'}),
                 ('action_confirm', {'locator': {'default': self.pop_up.locator(
                     '.ant-btn.ant-btn-primary.ant-btn-dangerous').first}, 'type': 'button'})],
                 'locator': {'default': self.page.locator('.ant-table-container').nth(0)},
                 'type': 'table_tr', }),
            ('policy', {'table': [
                ('add', {'locator': {'default': self.page.locator('.anticon.anticon-setting').first},
                         'type': 'button'}),
                ('sim1_threshold_enable',
                 {'locator': {'default': self.page.locator('#sim1_enabled')}, 'type': 'switch_button'}),
                ('sim1_threshold_input',
                 {'locator': {'default': self.page.locator('#sim1_threshold')}, 'type': 'fill'}),
                ('sim1_threshold_unit',
                 {'locator': {'default': self.page.locator('#sim1_threshold_unit')}, 'type': 'select',
                  'param': {'kb': 'KB', 'mb': 'MB', 'gb': 'GB'}}),
                ('sim1_monthly_reset_day',
                 {'locator': {'default': self.page.locator('#sim1_start_date')}, 'type': 'select'}),
                ('sim1_action',
                 {'locator': {'default': self.page.locator('#sim1_over_threshold_oper')}, 'type': 'select',
                  'param': {'notification': self.locale.notification,
                            'only_cloud_management_traffic': self.locale.only_cloud_management_traffic,
                            'switch_sim': self.locale.switch_sim}}),
                ('sim1_modify',
                 {'locator': {'default': self.page.locator('.ant-btn.ant-btn-link').nth(0)}, 'type': 'button'}),
                ('sim1_usage_of_the_month',
                 {'locator': {'default': self.page.locator('#sim1_adjust_usage')}, 'type': 'fill'}),
                ('sim1_usage_of_the_month_unit',
                 {'locator': {'default': self.page.locator('#sim1_adjust_usage_unit')}, 'type': 'select',
                  'param': {'kb': 'KB', 'mb': 'MB', 'gb': 'GB'}}),
                ('sim1_usage_of_the_month_confirm',
                 {'locator': {
                     'default': self.pop_up.locator(
                         'button[class="ant-btn ant-btn-primary"]:right-of(#sim1_adjust_usage_unit)').first},
                     'type': 'button'}),
                ('sim2_threshold_enable',
                 {'locator': {'default': self.page.locator('#sim2_enabled')}, 'type': 'switch_button'}),
                ('sim2_threshold_input',
                 {'locator': {'default': self.page.locator('#sim2_threshold')}, 'type': 'fill'}),
                ('sim2_threshold_unit',
                 {'locator': {'default': self.page.locator('#sim2_threshold_unit')}, 'type': 'select',
                  'param': {'kb': 'KB', 'mb': 'MB', 'gb': 'GB'}}),
                ('sim2_monthly_reset_day',
                 {'locator': {'default': self.page.locator('#sim2_start_date')}, 'type': 'select'}),
                ('sim2_action',
                 {'locator': {'default': self.page.locator('#sim2_over_threshold_oper')}, 'type': 'select',
                  'param': {'notification': self.locale.notification,
                            'only_cloud_management_traffic': self.locale.only_cloud_management_traffic,
                            'switch_sim': self.locale.switch_sim}}),
                ('sim2_modify',
                 {'locator': {'default': self.page.locator('.ant-btn.ant-btn-link').nth(1)}, 'type': 'button'}),
                ('sim2_usage_of_the_month',
                 {'locator': {'default': self.page.locator('#sim2_adjust_usage')}, 'type': 'fill'}),
                ('sim2_usage_of_the_month_unit',
                 {'locator': {'default': self.page.locator('#sim2_adjust_usage_unit')}, 'type': 'select',
                  'param': {'kb': 'KB', 'mb': 'MB', 'gb': 'GB'}}),
                ('sim2_usage_of_the_month_confirm',
                 {'locator': {'default': self.pop_up.locator(
                     'button[class="ant-btn ant-btn-primary"]:right-of(#sim2_adjust_usage_unit)').first},
                  'type': 'button'}),
                ('abnormal_card_switching_time',
                 {'locator': {'default': self.page.locator('#dial_timeout')}, 'type': 'fill'}),
                ('reuse_the_primary_card',
                 {'locator': {'default': self.page.locator('.ant-select-selection-overflow')},
                  'type': 'select_more',
                  'param': {'usage': self.locale.usage, 'time': self.locale.time, 'date': self.locale.date}}),
                ('usage_traffic',
                 {'locator': {'default': self.page.locator('#backup_sim_policy_usage_traffic_value')}, 'type': 'fill'}),
                ('usage_traffic_unit',
                 {'locator': {'default': self.page.locator('#backup_sim_policy_usage_traffic_unit')}, 'type': 'select',
                  'param': {'mb': 'MB', 'gb': 'GB'}}),
                ('using_time',
                 {'locator': {'default': self.page.locator('//input[@id="backup_sim_policy_using_time"]')},
                  'type': 'fill'}),
                ('switching_day_of_month',
                 {'locator': {'default': self.page.locator('#backup_sim_policy_revert_day')}, 'type': 'select'}),
                ('save', {'locator': self.pop_up.locator(
                    '//button[@class="ant-btn ant-btn-primary"]').last, 'type': 'button',
                          'wait_for': {'type': 'hidden', 'locator': self.pop_up, 'timeout': 300 * 1000}}),
                ('text_messages', {'type': 'text_messages'}),
                ('tip_messages', {'type': 'tip_messages'}),
                ('cancel',
                 {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-default"]'), 'type': 'button',
                  "always_do": True}),
                ('pop_up', {'locator': {'default': self.pop_up, 'default': self.pop_up}, 'type': 'button'}),
                ('action_confirm', {'locator': {'default': self.pop_up.locator('.ant-popover-inner-content').locator(
                    '.ant-btn.ant-btn-primary.ant-btn-sm.ant-btn-dangerous').first},
                                    'type': 'button'})],
                'locator': {'default': self.page.locator('.ant-table-container').nth(0)
                            },
                'type': 'table_tr', }),
            ('link_detection',
             {'locator': {'default': self.page.locator('#enabled')}, 'type': 'switch_button'}),
            ('detection_address_1',
             {'locator': {'default': self.page.locator('#target')}, 'type': 'fill'}),
            ('detection_address_2',
             {'locator': {'default': self.page.locator('#target2')}, 'type': 'fill'}),
            ('link_backup',
             {'locator': {'default': self.page.locator('#failover')}, 'type': 'radio'}),
            ('failover_mode',
             {'locator': {'default': self.page.locator('#switch_model')}, 'type': 'select',
              'param': {'immediately_switch': self.locale.immediately_switch,
                        'delayed_switch': self.locale.delayed_switch, 'do_not_switch': self.locale.do_not_switch}}),
            ('delay_number',
             {'locator': {'default': self.page.locator('#delay_num')}, 'type': 'fill',
              'relation': [('failover_mode', 'delayed_switch')]}),
            ('load_balancing',
             {'locator': {'default': self.page.locator('#load_balancing')}, 'type': 'radio'}),
            ('save', {'locator': self.page.locator(
                '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button',
                'wait_for': {'type': 'hidden', 'locator': self.pop_up, 'timeout': 300 * 1000}}),
            ('text_messages', {'type': 'text_messages'}),
            ('tip_messages', {'type': 'tip_messages'}),
            ('reset',
             {'locator': {'default': self.page.locator('//button[@class="ant-btn ant-btn-default"]').nth(1)},
              'type': 'button',
              "always_do": True})

        ]

    @property
    @AdaptModelLocator.adapt_model
    def inbound_rules(self) -> list:
        return [
            ('inbound_rules',
             {'grid': [
                 ('add', {'locator': {'default': self.page.locator('.anticon.anticon-plus').first},
                          'type': 'button'}),
                 ('name', {'locator': {'default': self.page.locator('#name')},
                           'type': 'fill'}),
                 ('status', {'locator': {'default': self.page.locator('#enabled')},
                             'type': 'switch_button'}),
                 ('interface', {'locator': {'default': self.page.locator('#interface')},
                                'type': 'select'}),
                 ('protocol', {'locator': {'default': self.page.locator('#protocol_select')},
                               'type': 'select', 'param': {'custom': self.locale.custom,
                                                           'tcp': 'TCP', 'udp': 'UDP', 'icmp': 'ICMP', 'any': 'Any'}}),
                 ('protocol_input', {'locator': {'default': self.page.locator('#protocol_input')},
                                     'type': 'fill', "relation": [('protocol', 'custom')]}),
                 ('source', {'locator': {'default': self.page.locator('#source_select')},
                             'type': 'select',
                             'param': {'any': 'Any', 'custom': self.locale.custom}}),
                 ('source_input', {'locator': {'default': self.page.locator('#source_input')},
                                   'type': 'fill', "relation": [('source', 'custom')]}),
                 ('src_port', {'locator': {'default': self.page.locator('#sport_select')},
                               'type': 'select',
                               'param': {'any': 'Any', 'custom': self.locale.custom}}),
                 ('src_port_input', {'locator': {'default': self.page.locator('#sport_input')},
                                     'type': 'fill', "relation": [('src_port', 'custom')]}),
                 ('destination', {'locator': {'default': self.page.locator('#destination_select')},
                                  'type': 'select',
                                  'param': {'any': 'Any', 'custom': self.locale.custom}}),
                 ('destination_input', {'locator': {'default': self.page.locator('#destination_input')},
                                        'type': 'fill', "relation": [('destination', 'custom')]}),
                 ('dst_port', {'locator': {'default': self.page.locator('#dport_select')},
                               'type': 'select',
                               'param': {'any': 'Any', 'custom': self.locale.custom}}),
                 ('dst_port_input', {'locator': {'default': self.page.locator('#dport_input')},
                                     'type': 'fill', "relation": [('src_port', 'custom')]}),
                 ('permit', {'locator': {'default': self.page.locator('//input[@value="permit"]')},
                             'type': 'check'}),
                 ('deny', {'locator': {'default': self.page.locator('//input[@value="deny"]')},
                           'type': 'check'}),
                 ('save', {'locator': self.page.locator(
                     '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button',
                     'wait_for': {'type': 'hidden', 'locator': self.pop_up, 'timeout': 300 * 1000}}),
                 ('text_messages', {'type': 'text_messages'}),
                 ('tip_messages', {'type': 'tip_messages'}),
                 ('cancel',
                  {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-default"]'), 'type': 'button',
                   "always_do": True}),
                 ('pop_up', {'locator': {'default': self.pop_up}, 'type': 'button'}),
                 ('action_confirm', {'locator': {'default': self.page.locator('.ant-popover-inner-content').locator(
                     '.ant-btn.ant-btn-primary.ant-btn-sm.ant-btn-dangerous').first},
                                     'type': 'button'})

             ],
                 'locator': {'default': self.page.locator('.ant-tabs-content.ant-tabs-content-top').nth(1)
                             },
                 'type': 'grid', }
             ),
        ]

    @property
    @AdaptModelLocator.adapt_model
    def ipsec_vpn(self) -> list:
        return [(
            'ipsec_vpn',
            {'table': [
                ('add', {'locator': {'default': self.page.locator('.anticon.anticon-plus').first},
                         'type': 'button'}),
                ('name', {'locator': {'default': self.page.locator('#name')},
                          'type': 'fill'}),
                ('status', {'locator': {'default': self.page.locator('#enabled')},
                            'type': 'switch_button'}),
                ('ike_version', {'locator': {'default': self.page.locator('#ike_version')},
                                 'type': 'select', 'param': {'ikev1': 'IKEv1', 'ikev2': 'IKEv2'}}),
                ('negotiation_mode', {'locator': {'default': self.page.locator('#ike_profile_ikev1_mode')},
                                      'type': 'select', 'param': {'main_mode': self.locale.main_mode,
                                                                  'agressive_mode': self.locale.agressive_mode},
                                      'relation': [('ike_version', 'ikev1')]}),
                ('pre_shared_key', {'locator': {'default': self.page.locator('#key')},
                                    'type': 'fill'}),
                ('uplink_interface', {'locator': {'default': self.page.locator('#interface')},
                                      'type': 'select'}),
                ('peer_address', {'locator': {'default': self.page.locator('#peeraddr')},
                                  'type': 'fill'}),
                ('tunnel_mode', {'locator': {'default': self.page.locator('#mode')},
                                 'type': 'select', 'param': {'tunnel': self.locale.tunnel,
                                                             'transmission': self.locale.transmission}}),
                ('local_subnet', {'locator': {'default': self.page.locator('#local_subnet_0')},
                                  'type': 'multi_fill'}),
                ('remote_subnet', {'locator': {'default': self.page.locator('#remote_subnet_0')},
                                   'type': 'multi_fill'}),
                ('local_identity', {'locator': {'default': self.page.locator('#ike_profile_lid_type')},
                                    'type': 'select', 'param': {'auto': self.locale.auto,
                                                                'ip_address': 'IP Address',
                                                                'fqdn': 'FQDN',
                                                                'user_fqdn': 'User FQDN', }}),
                ('local_identity_id', {'locator': {'default': self.page.locator('#ike_profile_local_id')},
                                       'type': 'fill'}),
                ('peer_identity', {'locator': {'default': self.page.locator('#ike_profile_rid_type')},
                                   'type': 'select', 'param': {'auto': self.locale.auto,
                                                               'ip_address': 'IP Address',
                                                               'fqdn': 'FQDN',
                                                               'user_fqdn': 'User FQDN', }}),
                ('peer_identity_id', {'locator': {'default': self.page.locator('#ike_profile_remote_id')},
                                      'type': 'fill'}),
                ('ike_policy_encryption', {'locator': {'default': self.page.locator('#ike_policy_encrypt')},
                                           'type': 'select', }),
                ('ike_policy_authentication', {'locator': {'default': self.page.locator('#ike_policy_auth')},
                                               'type': 'select', }),
                ('ike_policy_dh_groups', {'locator': {'default': self.page.locator('#ike_policy_dh')},
                                          'type': 'select', }),
                ('ike_policy_lifetime', {'locator': {'default': self.page.locator('#ike_policy_lifetime')},
                                         'type': 'fill'}),
                (
                    'ike_policy_peer_status_detect',
                    {'locator': {'default': self.page.locator('#ike_profile_dpd_enabled')},
                     'type': 'switch_button'}),
                ('ike_policy_dpd_interval', {'locator': {'default': self.page.locator('#ike_profile_dpd_interval')},
                                             'type': 'fill'}),
                ('ike_policy_dpd_timeout', {'locator': {'default': self.page.locator('#ike_profile_dpd_timeout')},
                                            'type': 'fill'}),
                ('ipsec_policy_security_protocol',
                 {'locator': {'default': self.page.locator('#ipsec_policy_sec_protocol')},
                  'type': 'select', }),
                ('ipsec_policy_encryption', {'locator': {'default': self.page.locator('#ipsec_policy_encrypt')},
                                             'type': 'select', }),
                ('ipsec_policy_authentication', {'locator': {'default': self.page.locator('#ipsec_policy_auth')},
                                                 'type': 'select', }),
                ('ipsec_policy_pfs_groups', {'locator': {'default': self.page.locator('#ipsec_policy_pfs')},
                                             'type': 'select', }),
                ('ipsec_policy_lifetime', {'locator': {'default': self.page.locator('#ipsec_policy_lifetime')},
                                           'type': 'fill'}),
                ('save', {'locator': self.page.locator(
                    '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button',
                    'wait_for': {'type': 'hidden', 'locator': self.pop_up, 'timeout': 300 * 1000}}),
                ('text_messages', {'type': 'text_messages'}),
                ('tip_messages', {'type': 'tip_messages'}),
                ('cancel',
                 {'locator': self.page.locator('//button[@class="ant-btn ant-btn-default"]'), 'type': 'button',
                  "always_do": True}),
                ('action_confirm', {'locator': {'default': self.page.locator('.ant-popover-inner-content').locator(
                    '.ant-btn.ant-btn-primary.ant-btn-sm.ant-btn-dangerous').first},
                                    'type': 'button'})],
                'locator': {'default': self.page.locator('.ant-table-container').nth(0)
                            },
                'type': 'table_tr', })
        ]

    @property
    @AdaptModelLocator.adapt_model
    def l2tp_vpn(self) -> list:
        return [
            ('status', {'locator': {'default': self.page.locator('#enabled')}, 'type': 'switch_button', }),
            ('uplink_interface', {'locator': {'default': self.page.locator('#interface')}, 'type': 'select', }),
            ('vpn_connection_address',
             {'locator': {'default': self.page.locator('#ip')}, 'type': 'fill', }),
            ('ip_pool_start',
             {'locator': {
                 'default': self.page.locator('//input[@type="text"]').nth(1)},
                 'type': 'fill', }),
            ('ip_pool_end',
             {'locator': {'default': self.page.locator('//input[@type="text"]').nth(2)}, 'type': 'fill', }),
            ('username',
             {'locator': {'default': self.page.locator('#username')}, 'type': 'fill', }),
            ('password',
             {'locator': {'default': self.page.locator('#password')}, 'type': 'fill', }),
            ('authentication_mode', {'locator': {'default': self.page.locator('#ppp_auth')}, 'type': 'select',
                                     'param': {'pap': 'PAP', 'chap': 'CHAP', 'auto': 'AUTO'}}),
            ('enable_tunnel_verification',
             {'locator': {'default': self.page.locator('#tunnel_auth_enabled')}, 'type': 'check', }),
            ('server_name',
             {'locator': {'default': self.page.locator('#tunnel_auth_server')}, 'type': 'fill',
              'relation': [('enable_tunnel_verification', 'check')]}),
            ('tunnel_verification_key',
             {'locator': {'default': self.page.locator('#tunnel_auth_password')}, 'type': 'fill',
              'relation': [('enable_tunnel_verification', 'check')]}),
            ('save', {'locator': self.page.locator(
                '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button',
                'wait_for': {'type': 'hidden', 'locator': self.pop_up, 'timeout': 300 * 1000}}),
            ('text_messages', {'type': 'text_messages'}),
            ('tip_messages', {'type': 'tip_messages'}),
            ('reset',
             {'locator': {'default': self.page.locator('//button[@class="ant-btn ant-btn-default"]')}, 'type': 'button',
              "always_do": True}),
            ('l2tp_client',
             {'table': [
                 ('add', {'locator': {'default': self.page.locator('.anticon.anticon-plus').first},
                          'type': 'button'}),
                 ('name', {'locator': {'default': self.page.locator('#alias')},
                           'type': 'fill'}),
                 ('status', {'locator': {'default': self.page.locator('#enabled')},
                             'type': 'switch_button'}),
                 ('uplink_interface', {'locator': {'default': self.page.locator('#interface')},
                                       'type': 'select'}),
                 ('server_address', {'locator': {'default': self.page.locator('#server_ip')},
                                     'type': 'fill'}),
                 ('username', {'locator': {'default': self.page.locator('#username')},
                               'type': 'fill', }),
                 ('password',
                  {'locator': {'default': self.page.locator('#password')}, 'type': 'fill', }),
                 ('authentication_mode', {'locator': {'default': self.page.locator('#ppp_auth')}, 'type': 'select',
                                          'param': {'pap': 'PAP', 'chap': 'CHAP', 'auto': 'AUTO'}}),
                 ('enable_tunnel_verification',
                  {'locator': {'default': self.page.locator('#tunnel_auth_enabled')}, 'type': 'check', }),
                 ('server_name',
                  {'locator': {'default': self.page.locator('#tunnel_auth_server')}, 'type': 'fill',
                   'relation': [('enable_tunnel_verification', 'check')]}),
                 ('tunnel_verification_key',
                  {'locator': {'default': self.page.locator('#tunnel_auth_password')}, 'type': 'fill',
                   'relation': [('enable_tunnel_verification', 'check')]}),
                 ('save', {'locator': self.page.locator(
                     '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button',
                     'wait_for': {'type': 'hidden', 'locator': self.pop_up, 'timeout': 300 * 1000}}),
                 ('text_messages', {'type': 'text_messages'}),
                 ('tip_messages', {'type': 'tip_messages'}),
                 ('cancel',
                  {'locator': self.page.locator('//button[@class="ant-btn ant-btn-default"]'), 'type': 'button',
                   "always_do": True}),
                 ('action_confirm', {'locator': {'default': self.page.locator('.ant-popover-inner-content').locator(
                     '.ant-btn.ant-btn-primary.ant-btn-sm.ant-btn-dangerous').first},
                                     'type': 'button'})],
                 'locator': {'default': self.page.locator('.ant-table-container').nth(0)
                             },
                 'type': 'table_tr', })
        ]

    @property
    @AdaptModelLocator.adapt_model
    def vxlan_vpn(self) -> list:
        return [
            ('vxlan_vpn',
             {'table': [
                 ('add', {'locator': {'default': self.page.locator('.anticon.anticon-plus').first},
                          'type': 'button'}),
                 ('name', {'locator': {'default': self.page.locator('#vxlanEditor_name')},
                           'type': 'fill'}),
                 ('status', {'locator': {'default': self.page.locator('#vxlanEditor_enabled')},
                             'type': 'switch_button'}),
                 ('uplink_interface', {'locator': {'default': self.page.locator('#vxlanEditor_interface')},
                                       'type': 'select'}),
                 ('peer_address', {'locator': {'default': self.page.locator('#vxlanEditor_remote')},
                                   'type': 'fill'}),
                 ('vni', {'locator': {'default': self.page.locator('#vxlanEditor_vni')},
                          'type': 'fill', }),
                 ('local_subnets', {'locator': {'default': self.page.locator('#vxlanEditor_vlan')},
                                    'type': 'select'}),
                 ('save', {'locator': self.page.locator(
                     '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button',
                     'wait_for': {'type': 'hidden', 'locator': self.pop_up, 'timeout': 300 * 1000}}),
                 ('text_messages', {'type': 'text_messages'}),
                 ('tip_messages', {'type': 'tip_messages'}),
                 ('cancel',
                  {'locator': self.page.locator('//button[@class="ant-btn ant-btn-default"]'), 'type': 'button',
                   "always_do": True}),
                 ('action_confirm', {'locator': {'default': self.page.locator('.ant-popover-inner-content').locator(
                     '.ant-btn.ant-btn-primary.ant-btn-sm.ant-btn-dangerous').first},
                                     'type': 'button'})],
                 'locator': {'default': self.page.locator('.ant-table-container').nth(0)
                             },
                 'type': 'table_tr', })
        ]

    @property
    @AdaptModelLocator.adapt_model
    def outbound_rules(self) -> list:
        return [
            ('outbound_rules',
             {'grid': [
                 ('add', {'locator': {'default': self.page.locator('.anticon.anticon-plus').first},
                          'type': 'button'}),
                 ('name', {'locator': {'default': self.page.locator('#name')},
                           'type': 'fill'}),
                 ('status', {'locator': {'default': self.page.locator('#enabled')},
                             'type': 'switch_button'}),
                 ('interface', {'locator': {'default': self.page.locator('#interface')},
                                'type': 'select'}),
                 ('protocol', {'locator': {'default': self.page.locator('#protocol_select')},
                               'type': 'select', 'param': {'custom': self.locale.custom,
                                                           'tcp': 'TCP', 'udp': 'UDP', 'icmp': 'ICMP', 'any': 'Any'}}),
                 ('protocol_input', {'locator': {'default': self.page.locator('#protocol_input')},
                                     'type': 'fill', "relation": [('protocol', 'custom')]}),
                 ('source', {'locator': {'default': self.page.locator('#source_select')},
                             'type': 'select',
                             'param': {'any': 'Any', 'custom': self.locale.custom}}),
                 ('source_input', {'locator': {'default': self.page.locator('#source_input')},
                                   'type': 'fill', "relation": [('source', 'custom')]}),
                 ('src_port', {'locator': {'default': self.page.locator('#sport_select')},
                               'type': 'select',
                               'param': {'any': 'Any', 'custom': self.locale.custom}}),
                 ('src_port_input', {'locator': {'default': self.page.locator('#sport_input')},
                                     'type': 'fill', "relation": [('src_port', 'custom')]}),
                 ('destination', {'locator': {'default': self.page.locator('#destination_select')},
                                  'type': 'select',
                                  'param': {'any': 'Any', 'custom': self.locale.custom}}),
                 ('destination_input', {'locator': {'default': self.page.locator('#destination_input')},
                                        'type': 'fill', "relation": [('destination', 'custom')]}),
                 ('dst_port', {'locator': {'default': self.page.locator('#dport_select')},
                               'type': 'select',
                               'param': {'any': 'Any', 'custom': self.locale.custom}}),
                 ('dst_port_input', {'locator': {'default': self.page.locator('#dport_input')},
                                     'type': 'fill', "relation": [('src_port', 'custom')]}),
                 ('permit', {'locator': {'default': self.page.locator('//input[@value="permit"]')},
                             'type': 'check'}),
                 ('deny', {'locator': {'default': self.page.locator('//input[@value="deny"]')},
                           'type': 'check'}),
                 ('save', {'locator': self.page.locator(
                     '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button',
                     'wait_for': {'type': 'hidden', 'locator': self.pop_up, 'timeout': 300 * 1000}}),
                 ('text_messages', {'type': 'text_messages'}),
                 ('tip_messages', {'type': 'tip_messages'}),
                 ('cancel',
                  {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-default"]'), 'type': 'button',
                   "always_do": True}),
                 ('pop_up', {'locator': {'default': self.pop_up}, 'type': 'button'}),
                 ('action_confirm', {'locator': {'default': self.page.locator('.ant-popover-inner-content').locator(
                     '.ant-btn.ant-btn-primary.ant-btn-sm.ant-btn-dangerous').first},
                                     'type': 'button'})

             ],
                 'locator': {'default': self.page.locator('.ant-tabs-content.ant-tabs-content-top').nth(1)
                             },
                 'type': 'grid', }
             ),
        ]

    @property
    @AdaptModelLocator.adapt_model
    def port_forwarding(self) -> list:
        return [
            ('port_forwarding',
             {'table': [
                 ('add', {'locator': {'default': self.page.locator('.anticon.anticon-plus').first},
                          'type': 'button'}),
                 ('name', {'locator': {'default': self.page.locator('#port_modal_name')},
                           'type': 'fill'}),
                 ('status', {'locator': {'default': self.page.locator('#port_modal_enabled')},
                             'type': 'switch_button'}),
                 ('interface', {'locator': {'default': self.page.locator('#port_modal_interface')},
                                'type': 'select'}),
                 ('protocol', {'locator': {'default': self.page.locator('#port_modal_protocol')},
                               'type': 'select', 'param': {'tcp': 'TCP', 'udp': 'UDP', 'tcp&udp': 'TCP&UDP'}}),
                 ('public_port', {'locator': {'default': self.page.locator('#port_modal_external_port')},
                                  'type': 'fill'}),
                 ('local_address', {'locator': {'default': self.page.locator('#port_modal_ip')},
                                    'type': 'fill', }),
                 ('local_port', {'locator': {'default': self.page.locator('#port_modal_internal_port')},
                                 'type': 'fill'}),
                 ('save', {'locator': self.page.locator(
                     '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button',
                     'wait_for': {'type': 'hidden', 'locator': self.pop_up, 'timeout': 300 * 1000}}),
                 ('text_messages', {'type': 'text_messages'}),
                 ('tip_messages', {'type': 'tip_messages'}),
                 ('cancel',
                  {'locator': self.page.locator('//button[@class="ant-btn ant-btn-default"]'), 'type': 'button',
                   "always_do": True}),
                 ('action_confirm', {'locator': {'default': self.page.locator('.ant-popover-inner-content').locator(
                     '.ant-btn.ant-btn-primary.ant-btn-sm.ant-btn-dangerous').first},
                                     'type': 'button'})],
                 'locator': {'default': self.page.locator('.ant-table-container').nth(0)
                             },
                 'type': 'table_tr', })
        ]

    @property
    @AdaptModelLocator.adapt_model
    def nat(self) -> list:
        return [
            ('input_name_query', {'locator': {'default': self.page.locator('#name')}, 'type': 'fill'}),
            ('input_ip_query', {'locator': {'default': self.page.locator('#ip')}, 'type': 'fill'}),
            ('input_port_query', {'locator': {'default': self.page.locator('#port')}, 'type': 'fill'}),
            ('reset',
             {'locator': {'default': self.page.locator('//button[@class="ant-btn ant-btn-primary"]')}, 'type': 'button',
              "always_do": True}),
            ('nat',
             {'table': [
                 ('add', {'locator': {'default': self.page.locator('.anticon.anticon-plus').first},
                          'type': 'button'}),
                 ('name', {'locator': {'default': self.page.locator('#natEditForm_name')},
                           'type': 'fill'}),
                 ('status', {'locator': {'default': self.page.locator('#natEditForm_enabled')},
                             'type': 'switch_button'}),
                 ('type', {'locator': {'default': self.page.locator('#natEditForm_type')},
                           'type': 'select'}),
                 ('protocol', {'locator': {'default': self.page.locator('#natEditForm_protocol')},
                               'type': 'select',
                               'param': {'tcp': 'TCP', 'udp': 'UDP', 'tcp&udp': 'TCP&UDP', 'any': 'Any'}}),
                 ('source',
                  {'locator': {
                      'default': self.page.locator(f'//label[@title="{self.locale.source}"]').locator(
                          '../..').locator('//input[@type="search"]')},
                      'type': 'select', 'param': {'any': 'Any', 'custom': self.locale.custom}}),
                 ('source_input',
                  {'locator': {
                      'default': self.page.locator(f'//label[@title="{self.locale.source}"]').locator(
                          '../..').locator('//input[@type="text"]')},
                      'type': 'fill', 'relation': [('source', 'custom')]}),
                 ('src_port',
                  {'locator': {
                      'default': self.page.locator(f'//label[@title="{self.locale.src_port}"]').locator(
                          '../..').locator('//input[@type="search"]')},
                      'type': 'select', 'param': {'any': 'Any', 'custom': self.locale.custom}}),
                 ('src_port_input',
                  {'locator': {
                      'default': self.page.locator(f'//label[@title="{self.locale.src_port}"]').locator(
                          '../..').locator('//input[@type="text"]')},
                      'type': 'fill', 'relation': [('src_port', 'custom')]}),
                 ('destination',
                  {'locator': {
                      'default': self.page.locator(f'//label[@title="{self.locale.destination}"]').locator(
                          '../..').locator('//input[@type="search"]')},
                      'type': 'select', 'param': {'any': 'Any', 'custom': self.locale.custom}}),
                 ('destination_input',
                  {'locator': {
                      'default': self.page.locator(f'//label[@title="{self.locale.destination}"]').locator(
                          '../..').locator('//input[@type="text"]')},
                      'type': 'fill', 'relation': [('destination', 'custom')]}),
                 ('dst_port',
                  {'locator': {
                      'default': self.page.locator(f'//label[@title="{self.locale.dst_port}"]').locator(
                          '../..').locator('//input[@type="search"]')},
                      'type': 'select', 'param': {'any': 'Any', 'custom': self.locale.custom}}),
                 ('dst_port_input',
                  {'locator': {
                      'default': self.page.locator(f'//label[@title="{self.locale.dst_port}"]').locator(
                          '../..').locator('//input[@type="text"]')},
                      'type': 'fill', 'relation': [('dst_port', 'custom')]}),
                 ('converted_address', {'locator': {'default': self.page.locator('#natEditForm_translation')},
                                        'type': 'fill', }),
                 ('converted_port',
                  {'locator': {
                      'default': self.page.locator(f'//label[@title="{self.locale.converted_port}"]').locator(
                          '../..').locator('//input[@type="search"]')},
                      'type': 'select', 'param': {'any': 'Any', 'custom': self.locale.custom}}),
                 ('converted_port_input',
                  {'locator': {
                      'default': self.page.locator(f'//label[@title="{self.locale.converted_port}"]').locator(
                          '../..').locator('//input[@type="text"]')},
                      'type': 'fill', 'relation': [('converted_port', 'custom')]}),
                 ('save', {'locator': self.pop_up.locator(
                     '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button',
                     'wait_for': {'type': 'hidden', 'locator': self.pop_up, 'timeout': 300 * 1000}}),
                 ('text_messages', {'type': 'text_messages'}),
                 ('tip_messages', {'type': 'tip_messages'}),
                 ('cancel',
                  {'locator': self.page.locator('//button[@class="ant-btn ant-btn-default"]'), 'type': 'button',
                   "always_do": True}),
                 ('action_confirm', {'locator': {'default': self.page.locator('.ant-popover-inner-content').locator(
                     '.ant-btn.ant-btn-primary.ant-btn-sm.ant-btn-dangerous').first},
                                     'type': 'button'})],
                 'locator': {'default': self.page.locator('.ant-table-container').nth(0)
                             },
                 'type': 'table_tr', })
        ]

    @property
    @AdaptModelLocator.adapt_model
    def mac_address_filter(self) -> list:
        return [
            ('unlimited',
             {'locator': {'default': self.page.locator('#macFilterListSet_mode').locator('.ant-radio-input').nth(0)},
              'type': 'radio'}),
            ('blacklist',
             {'locator': {'default': self.page.locator('#macFilterListSet_mode').locator('.ant-radio-input').nth(1)},
              'type': 'radio'}),
            ('whitelist',
             {'locator': {'default': self.page.locator('#macFilterListSet_mode').locator('.ant-radio-input').nth(2)},
              'type': 'radio'}),
            ('save',
             {'locator': {'default': self.page.locator(
                 '//button[@class="ant-btn ant-btn-primary"]')}, 'type': 'button'}),
            ('reset',
             {'locator': {'default': self.page.locator('//button[@class="ant-btn ant-btn-primary"]')}, 'type': 'button',
              "always_do": True}),
            ('mac_address_list',
             {'table': [
                 ('add', {'locator': {'default': self.page.locator('.anticon.anticon-plus').first},
                          'type': 'button'}),
                 ('mac_address', {'locator': {'default': self.page.locator('//input[@type="text"]').nth(0)},
                                  'type': 'fill'}),
                 ('status', {'locator': {'default': self.page.locator('//button[@role="switch"]')},
                             'type': 'switch_button'}),
                 ('description', {'locator': {'default': self.page.locator('//input[@type="text"]').nth(1)},
                                  'type': 'fill'}),
                 ('save', {'locator': self.page.locator('.anticon.anticon-save'), 'type': 'button'}),
                 ('text_messages', {'type': 'text_messages'}),
                 ('tip_messages', {'type': 'tip_messages'}),
                 ('cancel',
                  {'locator': self.page.locator('//button[@class="ant-btn ant-btn-default"]'), 'type': 'button',
                   "always_do": True}),
                 ('action_confirm', {'locator': {'default': self.page.locator('.ant-popover-inner-content').locator(
                     '.ant-btn.ant-btn-primary.ant-btn-sm.ant-btn-dangerous').first},
                                     'type': 'button'})],
                 'locator': {'default': self.page.locator('.ant-table-container').nth(0)
                             },
                 'type': 'table_tr', })
        ]

    @property
    @AdaptModelLocator.adapt_model
    def domin_name_filter(self) -> list:
        return [
            ('unlimited',
             {'locator': {'default': self.page.locator('#domainFilterListSet_mode').locator('.ant-radio-input').nth(0)},
              'type': 'radio'}),
            ('blacklist',
             {'locator': {'default': self.page.locator('#domainFilterListSet_mode').locator('.ant-radio-input').nth(1)},
              'type': 'radio'}),
            ('whitelist',
             {'locator': {'default': self.page.locator('#domainFilterListSet_mode').locator('.ant-radio-input').nth(2)},
              'type': 'radio'}),
            ('save',
             {'locator': {'default': self.page.locator(
                 '//button[@class="ant-btn ant-btn-primary"]')}, 'type': 'button'}),
            ('text_messages', {'type': 'text_messages'}),
            ('tip_messages', {'type': 'tip_messages'}),
            ('reset',
             {'locator': {'default': self.page.locator('//button[@class="ant-btn ant-btn-primary"]')}, 'type': 'button',
              "always_do": True}),
            ('domin_name_list',
             {'table': [
                 ('add', {'locator': {'default': self.page.locator('.anticon.anticon-plus').first},
                          'type': 'button'}),
                 ('domains', {'locator': {'default': self.page.locator('//input[@type="text"]').nth(0)},
                              'type': 'fill'}),
                 ('description', {'locator': {'default': self.page.locator('//input[@type="text"]').nth(1)},
                                  'type': 'fill'}),
                 ('save', {'locator': self.page.locator('.anticon.anticon-save'), 'type': 'button'}),
                 ('text_messages', {'type': 'text_messages'}),
                 ('tip_messages', {'type': 'tip_messages'}),
                 ('cancel',
                  {'locator': self.page.locator('//button[@class="ant-btn ant-btn-default"]'), 'type': 'button',
                   "always_do": True}),
                 ('action_confirm', {'locator': {'default': self.page.locator('.ant-popover-inner-content').locator(
                     '.ant-btn.ant-btn-primary.ant-btn-sm.ant-btn-dangerous').first},
                                     'type': 'button'})],
                 'locator': {'default': self.page.locator('.ant-table-container').nth(0)
                             },
                 'type': 'table_tr', })
        ]

    @property
    @AdaptModelLocator.adapt_model
    def policy_based_routing(self) -> list:
        return [
            ('policy_based_routing',
             {'grid': [
                 ('add', {'locator': {'default': self.page.locator('.anticon.anticon-plus').first},
                          'type': 'button'}),
                 ('name', {'locator': {'default': self.page.locator('#name')},
                           'type': 'fill'}),
                 ('status', {'locator': {'default': self.page.locator('#enabled')},
                             'type': 'switch_button'}),
                 ('protocol', {'locator': {'default': self.page.locator('#protocol_select')},
                               'type': 'select', 'param': {'tcp': 'TCP', 'udp': 'UDP', 'any': 'Any', 'icmp': 'ICMP',
                                                           'custom': self.locale.custom}}),
                 ('protocol_input', {'locator': {'default': self.page.locator('#protocol_input')},
                                     'type': 'fill', 'relation': [('protocol', 'custom')]}),
                 ('source', {'locator': {'default': self.page.locator('#source_select')},
                             'type': 'select', 'param': {'any': 'Any', 'custom': self.locale.custom}}),
                 ('source_input', {'locator': {'default': self.page.locator('#source_input')},
                                   'type': 'fill', 'relation': [('source', 'custom')]}),
                 ('src_port', {'locator': {'default': self.page.locator('#sport_select')},
                               'type': 'select', 'param': {'any': 'Any', 'custom': self.locale.custom}}),
                 ('src_port_input', {'locator': {'default': self.page.locator('#sport_input')},
                                     'type': 'fill', 'relation': [('src_port', 'custom')]}),
                 ('destination', {'locator': {'default': self.page.locator('#destination_select')},
                                  'type': 'select', 'param': {'any': 'Any', 'custom': self.locale.custom}}),
                 ('destination_input', {'locator': {'default': self.page.locator('#destination_input')},
                                        'type': 'fill', 'relation': [('destination', 'custom')]}),
                 ('dst_port', {'locator': {'default': self.page.locator('#dport_select')},
                               'type': 'select', 'param': {'any': 'Any', 'custom': self.locale.custom}}),
                 ('dst_port_input', {'locator': {'default': self.page.locator('#dport_input')},
                                     'type': 'fill', 'relation': [('dst_port', 'custom')]}),
                 ('output', {'locator': {'default': self.page.locator('#preferred_outif')},
                             'type': 'select', 'param': {'any': 'Any', 'custom': self.locale.custom}}),
                 ('forced_forwarding', {'locator': {'default': self.page.locator('#force_forward')},
                                        'type': 'check'}),
                 ('save', {'locator': self.page.locator(
                     '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button',
                     'wait_for': {'type': 'hidden', 'locator': self.pop_up, 'timeout': 300 * 1000}}),
                 ('text_messages', {'type': 'text_messages'}),
                 ('tip_messages', {'type': 'tip_messages'}),
                 ('cancel',
                  {'locator': self.page.locator('//button[@class="ant-btn ant-btn-default"]'), 'type': 'button',
                   "always_do": True}),
                 ('action_confirm', {'locator': {'default': self.page.locator('.ant-popover-inner-content').locator(
                     '.ant-btn.ant-btn-primary.ant-btn-sm.ant-btn-dangerous').first},
                                     'type': 'button'})],
                 'locator': {'default': self.page.locator('.ant-pro-grid-content-children').nth(0)
                             },
                 'type': 'grid', })
        ]

    @property
    @AdaptModelLocator.adapt_model
    def traffic_shaping(self) -> list:
        return [
            ('uplink_bandwidth',
             {'table': [
                 ('up_bandwidth', {'locator': {'default': self.page.locator('.ant-input').first},
                                   'type': 'fill'}),
                 ('up_bandwidth_unit',
                  {'locator': {'default': self.page.locator('.ant-select-selection-search-input').first},
                   'type': 'select'}),
                 ('down_bandwidth', {'locator': {'default': self.page.locator('.ant-input').last},
                                     'type': 'fill', }),
                 (
                     'down_bandwidth_unit',
                     {'locator': {'default': self.page.locator('.ant-select-selection-search-input').last},
                      'type': 'select'}),
                 ('save', {'locator': self.page.locator(
                     '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button',
                     'wait_for': {'type': 'hidden', 'locator': self.pop_up, 'timeout': 300 * 1000}}),
                 ('text_messages', {'type': 'text_messages'}),
                 ('tip_messages', {'type': 'tip_messages'}),
                 ('cancel',
                  {'locator': self.page.locator('//button[@class="ant-btn ant-btn-default"]'), 'type': 'button',
                   "always_do": True})],
                 'locator': {'default': self.page.locator('.uplinkBandwidthContainer___YUWpO').nth(0)
                             },
                 'type': 'table_tr', }),
            ('shaping_rules',
             {'grid': [
                 ('add', {'locator': {'default': self.page.locator('.anticon.anticon-plus').first},
                          'type': 'button'}),
                 ('name', {'locator': {'default': self.page.locator('#name')},
                           'type': 'fill'}),
                 ('status', {'locator': {'default': self.page.locator('#enabled')},
                             'type': 'switch_button'}),
                 ('protocol', {'locator': {'default': self.page.locator('#protocol_select')},
                               'type': 'select', 'param': {'tcp': 'TCP', 'udp': 'UDP', 'any': 'Any', 'icmp': 'ICMP',
                                                           'custom': self.locale.custom}}),
                 ('protocol_input', {'locator': {'default': self.page.locator('#protocol_input')},
                                     'type': 'fill', 'relation': [('protocol', 'custom')]}),
                 ('source', {'locator': {'default': self.page.locator('#source_select')},
                             'type': 'select', 'param': {'any': 'Any', 'custom': self.locale.custom}}),
                 ('source_input', {'locator': {'default': self.page.locator('#source_input')},
                                   'type': 'fill', 'relation': [('source', 'custom')]}),
                 ('src_port', {'locator': {'default': self.page.locator('#sport_select')},
                               'type': 'select', 'param': {'any': 'Any', 'custom': self.locale.custom}}),
                 ('src_port_input', {'locator': {'default': self.page.locator('#sport_input')},
                                     'type': 'fill', 'relation': [('src_port', 'custom')]}),
                 ('destination', {'locator': {'default': self.page.locator('#destination_select')},
                                  'type': 'select', 'param': {'any': 'Any', 'custom': self.locale.custom}}),
                 ('destination_input', {'locator': {'default': self.page.locator('#destination_input')},
                                        'type': 'fill', 'relation': [('destination', 'custom')]}),
                 ('dst_port', {'locator': {'default': self.page.locator('#dport_select')},
                               'type': 'select', 'param': {'any': 'Any', 'custom': self.locale.custom}}),
                 ('dst_port_input', {'locator': {'default': self.page.locator('#dport_input')},
                                     'type': 'fill', 'relation': [('dst_port', 'custom')]}),
                 ('priority', {'locator': {'default': self.page.locator('#priority')},
                               'type': 'select', 'param': {'highest': self.locale.highest, 'high': self.locale.high,
                                                           'medium': self.locale.medium, 'low': self.locale.low,
                                                           'lowest': self.locale.lowest}}),
                 ('dscp_tags', {'locator': {'default': self.page.locator('#dscp')},
                                'type': 'select', 'param': {'no_dscp': self.locale.no_dscp, '10': self.locale.dscp_10,
                                                            '12': self.locale.dscp_12, '14': self.locale.dscp_14,
                                                            '18': self.locale.dscp_18, '20': self.locale.dscp_20,
                                                            '22': self.locale.dscp_22, '26': self.locale.dscp_26,
                                                            '28': self.locale.dscp_28, '30': self.locale.dscp_30,
                                                            '34': self.locale.dscp_34, '36': self.locale.dscp_36,
                                                            '38': self.locale.dscp_38, '0': self.locale.dscp_0,
                                                            '8': self.locale.dscp_8, '16': self.locale.dscp_16,
                                                            '24': self.locale.dscp_24, '32': self.locale.dscp_32,
                                                            '40': self.locale.dscp_40, '46': self.locale.dscp_46,
                                                            '48': self.locale.dscp_48, '56': self.locale.dscp_56,
                                                            '44': self.locale.dscp_44, }}),
                 ('limit_bandwidth_up', {'locator': {'default': self.page.locator(
                     '//span[@class="ant-input-group ant-input-group-compact"]').nth(0).locator(
                     '//input[@type="text"]')},
                     'type': 'fill'}),
                 ('limit_bandwidth_up_unit', {'locator': {'default': self.page.locator(
                     '//span[@class="ant-input-group ant-input-group-compact"]').nth(0).locator(
                     '//input[@type="search"]')},
                     'type': 'select'}),
                 ('limit_bandwidth_down', {'locator': {'default': self.page.locator(
                     '//span[@class="ant-input-group ant-input-group-compact"]').nth(1).locator(
                     '//input[@type="text"]')},
                     'type': 'fill'}),
                 ('limit_bandwidth_down_unit', {'locator': {'default': self.page.locator(
                     '//span[@class="ant-input-group ant-input-group-compact"]').nth(1).locator(
                     '//input[@type="search"]')},
                     'type': 'select'}),
                 ('reserved_bandwidth_up', {'locator': {'default': self.page.locator(
                     '//span[@class="ant-input-group ant-input-group-compact"]').nth(2).locator(
                     '//input[@type="text"]')},
                     'type': 'fill'}),
                 ('reserved_bandwidth_up_unit', {'locator': {'default': self.page.locator(
                     '//span[@class="ant-input-group ant-input-group-compact"]').nth(2).locator(
                     '//input[@type="search"]')},
                     'type': 'select'}),
                 ('reserved_bandwidth_down', {'locator': {'default': self.page.locator(
                     '//span[@class="ant-input-group ant-input-group-compact"]').nth(3).locator(
                     '//input[@type="text"]')},
                     'type': 'fill'}),
                 ('reserved_bandwidth_down_unit', {'locator': {'default': self.page.locator(
                     '//span[@class="ant-input-group ant-input-group-compact"]').nth(3).locator(
                     '//input[@type="search"]')},
                     'type': 'select'}),
                 ('save', {'locator': self.page.locator(
                     '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button',
                     'wait_for': {'type': 'hidden', 'locator': self.pop_up, 'timeout': 300 * 1000}}),
                 ('text_messages', {'type': 'text_messages'}),
                 ('tip_messages', {'type': 'tip_messages'}),
                 ('cancel',
                  {'locator': self.page.locator('//button[@class="ant-btn ant-btn-default"]'), 'type': 'button',
                   "always_do": True}),
                 ('action_confirm', {'locator': {'default': self.page.locator('.ant-popover-inner-content').locator(
                     '.ant-btn.ant-btn-primary.ant-btn-sm.ant-btn-dangerous').first},
                                     'type': 'button'})],
                 'locator': {'default': self.page.locator('.shapingRulesContainer___2UYAV').nth(0)
                             },
                 'type': 'grid', })
        ]

    @property
    @AdaptModelLocator.adapt_model
    def interface_management(self) -> list:
        return [
            ('expand', {'locator': {'default': self.locale.interface_management}, 'type': 'expand'},),
            ('interface_management',
             {'table': [
                 ('status', {'locator': {'default': self.pop_up.locator('#enabled')},
                             'type': 'switch_button'}),
                 ('network', {'locator': {'default': self.page.locator('#network')},
                              'type': 'select', 'param': {'all': self.locale.all}}),
                 ('link_rate', {'locator': {'default': self.page.locator('#link_rate')},
                                'type': 'select', 'param': {'auto': self.locale.auto,
                                                            'full_1000mbps_duplex': self.locale.full_1000mbps_duplex,
                                                            'full_100mbps_duplex': self.locale.full_100mbps_duplex,
                                                            'full_10mbps_duplex': self.locale.full_10mbps_duplex,
                                                            'half_100mbps_duplex': self.locale.half_100mbps_duplex,
                                                            'half_10mbps_duplex': self.locale.half_10mbps_duplex}}),
                 ('save', {'locator': self.pop_up.locator(
                     '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button',
                     'wait_for': {'type': 'hidden', 'locator': self.pop_up, 'timeout': 300 * 1000}}),
                 ('text_messages', {'type': 'text_messages'}),
                 ('tip_messages', {'type': 'tip_messages'}),
                 ('cancel',
                  {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-default"]'), 'type': 'button',
                   "always_do": True}),
                 ('action_confirm', {'locator': {'default': self.page.locator('.ant-popover-inner-content').locator(
                     '.ant-btn.ant-btn-primary.ant-btn-sm.ant-btn-dangerous').first},
                                     'type': 'button'})],
                 'locator': {
                     'default': self.page.locator(f'table:below(:text-is("{self.locale.interface_management}"))').first
                 },
                 'type': 'table_tr', })
        ]

    @property
    @AdaptModelLocator.adapt_model
    def dhcp_server(self) -> list:
        return [
            ('expand', {'locator': {'default': self.locale.dhcp_server}, 'type': 'expand'},),
            ('dhcp_server',
             {'table': [
                 ('status', {'locator': {'default': self.pop_up.locator('#enabled')},
                             'type': 'switch_button'}),
                 ('dhcp_ip_range_start',
                  {'locator': {'default': self.page.locator('.ant-input').nth(0)},
                   'type': 'fill', }),
                 ('dhcp_ip_range_end',
                  {'locator': {'default': self.page.locator('.ant-input').nth(1)},
                   'type': 'fill', }),
                 ('lease', {'locator': {'default': self.pop_up.locator('#lease')},
                            'type': 'select', 'param': {'1_day': self.locale.day_1, '1_hour': self.locale.hour_1,
                                                        '1_week': self.locale.week_1, '6_hours': self.locale.hours_6,
                                                        '12_hours': self.locale.hours_12}}),
                 ('dns', {'locator': {'default': self.page.locator('#option_dns_type')},
                          'type': 'select', 'param': {'auto': self.locale.auto, 'manual': self.locale.manual}}),
                 ('main_dns',
                  {'locator': {'default': self.page.locator('#option_dns1')}, 'type': 'fill',
                   'relation': [('dns', 'manual')]}),
                 ('secondary_dns',
                  {'locator': {'default': self.page.locator('#option_dns2')}, 'type': 'fill',
                   'relation': [('dns', 'manual')]}),
                 ('save', {'locator': self.pop_up.locator(
                     '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button',
                     'wait_for': {'type': 'hidden', 'locator': self.pop_up, 'timeout': 300 * 1000}}),
                 ('text_messages', {'type': 'text_messages'}),
                 ('tip_messages', {'type': 'tip_messages'}),
                 ('cancel',
                  {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-default"]'), 'type': 'button',
                   "always_do": True}),
                 ('action_confirm', {'locator': {'default': self.page.locator('.ant-popover-inner-content').locator(
                     '.ant-btn.ant-btn-primary.ant-btn-sm.ant-btn-dangerous').first},
                                     'type': 'button'})],
                 'locator': {
                     'default': self.page.locator(f'table:below(:text-is("{self.locale.dhcp_server}"))').first
                 },
                 'type': 'table_tr', })
        ]

    @property
    @AdaptModelLocator.adapt_model
    def dns_server(self) -> list:
        return [
            ('expand', {'locator': {'default': self.locale.dns_server}, 'type': 'expand'},),
            ('dns_server1', {'locator': {'default': self.page.locator('#dnsServerForm_dns1')},
                             'type': 'fill'}),
            ('dns_server2', {'locator': {'default': self.page.locator('#dnsServerForm_dns2')},
                             'type': 'fill'}),
            ('save', {'locator': self.page.locator(
                f'button:has-text("{self.locale.save}"):below(:text-is("{self.locale.dns_server}"))').first,
                      'type': 'button'}),
            ('text_messages', {'type': 'text_messages'}),
            ('tip_messages', {'type': 'tip_messages'}),
            ('reset',
             {'locator': self.page.locator(
                 f'button:text-is("{self.locale.reset}"):below(:text-is("{self.locale.dns_server}"))'),
                 'type': 'button',
                 "always_do": True}),
        ]

    @property
    @AdaptModelLocator.adapt_model
    def fixed_address_list(self) -> list:
        return [
            ('expand', {'locator': {'default': self.locale.fixed_address_list}, 'type': 'expand'},),
            ('network', {'locator': {'default': self.page.locator(
                f'input:below(:text-is("{self.locale.fixed_address_list}"))').nth(0)}, 'type': 'select',
                         'param': {'all_network': self.locale.all_network}},),
            ('filter_select', {'locator': {'default': self.page.locator(
                f'input:below(:text-is("{self.locale.fixed_address_list}"))').nth(1)}, 'type': 'select',
                               'param': {'ip_address': self.locale.ip_address, 'mac_address': self.locale.mac_address,
                                         'clients': self.locale.clients}},),
            ('filter_input', {'locator': {'default': self.page.locator(
                f'input:below(:text-is("{self.locale.fixed_address_list}"))').nth(2)}, 'type': 'fill'},),
            ('fixed_address_list',
             {'table': [
                 ('add', {'locator': {'default': self.page.locator(
                     f'button:has-text("{self.locale.add}"):below(:text-is("{self.locale.fixed_address_list}"))').first},
                          'type': 'button'}),
                 ('network', {'locator': {'default': self.page.locator('#server')}, 'type': 'select'}),
                 ('mac_address', {'locator': {'default': self.page.locator('#mac')}, 'type': 'fill'}),
                 ('ip_address', {'locator': {'default': self.page.locator('#ip')}, 'type': 'fill'}),
                 ('clients', {'locator': {'default': self.page.locator('#hostname')}, 'type': 'fill'}),
                 ('save', {'locator': self.page.locator('.anticon.anticon-save'), 'type': 'click'}),
                 ('text_messages', {'type': 'text_messages'}),
                 ('tip_messages', {'type': 'tip_messages'}),
                 ('cancel',
                  {'locator': self.page.locator('.anticon.anticon-close'), 'type': 'click',
                   "always_do": True}),
                 ('action_confirm', {'locator': {'default': self.page.locator('.ant-popover-inner-content').locator(
                     '.ant-btn.ant-btn-primary.ant-btn-sm.ant-btn-dangerous').first},
                                     'type': 'button'})],
                 'locator': {
                     'default': self.page.locator(f'table:below(:text-is("{self.locale.fixed_address_list}"))').first
                 },
                 'type': 'table_tr', })
        ]

    @property
    @AdaptModelLocator.adapt_model
    def static_routes(self) -> list:
        return [
            ('expand', {'locator': {'default': self.locale.static_routes}, 'type': 'expand'},),
            ('static_routes',
             {'table': [
                 ('add', {'locator': {'default': self.page.locator(
                     f'button:has-text("{self.locale.add}"):below(:text-is("{self.locale.static_routes}"))').first},
                          'type': 'button'}),
                 ('dest_add_net', {'locator': {'default': self.page.locator('#destination')},
                                   'type': 'fill'}),
                 ('type', {'locator': {'default': self.page.locator('#type')},
                           'type': 'select',
                           'param': {'next_hop': self.locale.next_hop, 'interface': self.locale.interface}}),
                 ('next_hop', {'locator': {'default': self.page.locator('#gateway')},
                               'type': 'fill', 'relation': [('type', 'next_hop')]}),
                 ('interface', {'locator': {'default': self.pop_up.locator('#interface')},
                                'type': 'select', 'relation': [('type', 'interface')]}),
                 ('priority',
                  {'locator': {'default': self.page.locator('#distance')}, 'type': 'fill', }),
                 ('description',
                  {'locator': {'default': self.page.locator('#desc')}, 'type': 'fill', }),
                 ('save', {'locator': self.pop_up.locator(
                     '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button',
                     'wait_for': {'type': 'hidden', 'locator': self.pop_up, 'timeout': 300 * 1000}}),
                 ('text_messages', {'type': 'text_messages'}),
                 ('tip_messages', {'type': 'tip_messages'}),
                 ('cancel',
                  {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-default"]'), 'type': 'button',
                   "always_do": True}),
                 ('action_confirm', {'locator': {'default': self.page.locator('.ant-popover-inner-content').locator(
                     '.ant-btn.ant-btn-primary.ant-btn-sm.ant-btn-dangerous').first},
                                     'type': 'button'})],
                 'locator': {
                     'default': self.page.locator(f'table:below(:text-is("{self.locale.dhcp_server}"))').first
                 },
                 'type': 'table_tr', })
        ]

    @property
    @AdaptModelLocator.adapt_model
    def dynamic_dns(self) -> list:
        return [
            ('expand', {'locator': {'default': self.locale.dynamic_dns}, 'type': 'expand'},),
            ('dynamic_dns',
             {'table': [
                 ('add', {'locator': {'default': self.page.locator(
                     f'button:has-text("{self.locale.add}"):below(:text-is("{self.locale.dynamic_dns}"))').first},
                          'type': 'button'}),
                 ('service_provider', {'locator': {'default': self.page.locator('#ddnsForm_provider')},
                                       'type': 'select', 'param': {'custom': self.locale.custom, }}),
                 ('url_address', {'locator': {'default': self.page.locator('#ddnsForm_url')}, 'type': 'fill',
                                  'relation': [('service_provider', 'custom')]}),
                 ('hostname', {'locator': {'default': self.page.locator('#ddnsForm_hostname')}, 'type': 'fill'}),
                 ('username', {'locator': {'default': self.page.locator('#ddnsForm_username')}, 'type': 'fill'}),
                 ('password', {'locator': {'default': self.page.locator('#ddnsForm_password')}, 'type': 'fill'}),
                 ('update_time', {'locator': {'default': self.page.locator('#ddnsForm_update_period')},
                                  'type': 'fill'}),
                 ('update_interface', {'locator': {'default': self.page.locator('#ddnsForm_interface')},
                                       'type': 'select'}),
                 ('save', {'locator': self.pop_up.locator(
                     '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button',
                     'wait_for': {'type': 'hidden', 'locator': self.pop_up, 'timeout': 300 * 1000}}),
                 ('text_messages', {'type': 'text_messages'}),
                 ('tip_messages', {'type': 'tip_messages'}),
                 ('cancel',
                  {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-default"]'), 'type': 'button',
                   "always_do": True}),
                 ('action_confirm', {'locator': {'default': self.page.locator('.ant-popover-inner-content').locator(
                     '.ant-btn.ant-btn-primary.ant-btn-sm.ant-btn-dangerous').first},
                                     'type': 'button'})],
                 'locator': {
                     'default': self.page.locator(f'table:below(:text-is("{self.locale.dhcp_server}"))').first
                 },
                 'type': 'table_tr', })
        ]

    @property
    @AdaptModelLocator.adapt_model
    def passthrough_settings(self) -> list:
        return [
            ('expand', {'locator': {'default': self.locale.passthrough_settings}, 'type': 'expand'},),
            ('ip_passthrough', {'locator': {'default': self.page.locator('#enabled')}, 'type': 'switch_button'},),
            ('passthrough_mac', {'locator': {'default': self.page.locator('#bind_mac')}, 'type': 'fill'},),
            ('passthrough_wan', {'locator': {'default': self.page.locator('#uplink')},
                                 'type': 'select', }),
            ('passthrough_lan', {'locator': {'default': self.page.locator('#downlink')},
                                 'type': 'select', }),
            ('dhcp_server', {'locator': {'default': self.page.locator('#dhcp_enabled')}, 'type': 'check'},),
            ('lease', {'locator': {'default': self.page.locator('#lease')},
                       'type': 'select', 'param': {'1_day': self.locale.day_1, '1_hour': self.locale.hour_1,
                                                   '1_week': self.locale.week_1, '6_hours': self.locale.hours_6,
                                                   '12_hours': self.locale.hours_12}}),
            ('save', {'locator': self.page.locator(
                f'button:has-text("{self.locale.save}"):below(:text-is("{self.locale.dns_server}"))').first,
                      'type': 'button'}),
            ('text_messages', {'type': 'text_messages'}),
            ('tip_messages', {'type': 'tip_messages'}),
            ('reset',
             {'locator': self.page.locator(
                 f'button:text-is("{self.locale.reset}"):below(:text-is("{self.locale.passthrough_settings}"))'),
                 'type': 'button',
                 "always_do": True}),
        ]

    @property
    @AdaptModelLocator.adapt_model
    def cloud_management(self) -> list:
        return [
            ('cloud_management', {'locator': {'default': self.locale.cloud_management}, 'type': 'expand'}),
            ('enabled_cloud_management', {'locator': {'default': self.page.locator('#cloudManage_cloud_enabled')},
                                          'type': 'switch_button'}),
            ('cloud_platform', {'locator': {'default': self.page.locator('#cloudManage_server')}, 'type': 'select',
                                'param': {'incloud_manager_china': self.locale.incloud_manager_china,
                                          'incloud_manager_global': self.locale.incloud_manager_global}}),
            ('mqtt_keepalive_time', {'locator': {'default': self.page.locator('#cloudManage_mqtt_keepalive')},
                                     'type': 'fill'}),
            ('log_reporting', {'locator': {'default': self.page.locator('#cloudManage_log_cloud')},
                               'type': 'switch_button'}),
            ('save', {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'}),
            ('text_messages', {'type': 'text_messages'}),
            ('tip_messages', {'type': 'tip_messages'}),
            ('reset', {'locator': self.page.locator('//button[@class="ant-btn ant-btn-default"]'),
                       'type': 'button', "always_do": True}),
        ]

    @property
    @AdaptModelLocator.adapt_model
    def remote_access_control(self) -> list:
        return [
            ('remote_access_control', {'locator': {'default': self.locale.remote_access_control}, 'type': 'expand'}),
            ('enable_https', {'locator': {'default': self.page.locator('#webAccess_https_enabled')},
                              'type': 'switch_button'}),
            ('https_port', {'locator': {'default': self.page.locator('#webAccess_https_port')}, 'type': 'fill'}),
            ('enable_ssh', {'locator': {'default': self.page.locator('#webAccess_ssh_enabled')},
                            'type': 'switch_button'}),
            ('ssh_port', {'locator': {'default': self.page.locator('#webAccess_ssh_port')}, 'type': 'fill'}),
            ('enable_ping', {'locator': {'default': self.page.locator('#webAccess_ping_enabled')},
                             'type': 'switch_button'}),
            ('save', {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'}),
            ('text_messages', {'type': 'text_messages'}),
            ('tip_messages', {'type': 'tip_messages'}),
            ('reset', {'locator': {'default': self.page.locator('//button[@class="ant-btn ant-btn-default"]')},
                       'type': 'button', "always_do": True}),
        ]

    @property
    @AdaptModelLocator.adapt_model
    def system_clock(self) -> list:
        return [
            ('system_clock', {'locator': {'default': self.locale.system_clock}, 'type': 'expand'}),
            ('time_zone', {'locator': {'default': self.page.locator('#systemClock_timezone')}, 'type': 'select',
                           'param': {
                               "kwajalein": self.locale.kwajalein,
                               "midway_island": self.locale.midway_island,
                               "hawaii": self.locale.hawaii,
                               "alaska": self.locale.alaska,
                               "pacific": self.locale.pacific,
                               "arizona": self.locale.arizona,
                               "rocky_mountains": self.locale.rocky_mountains,
                               "mexico": self.locale.mexico,
                               "central_time": self.locale.central_time,
                               "colombia": self.locale.colombia,
                               "eastern_time": self.locale.eastern_time,
                               "bolivia": self.locale.bolivia,
                               "atlantic_time": self.locale.atlantic_time,
                               "brazil_west": self.locale.brazil_west,
                               "newfoundland": self.locale.newfoundland,
                               "greenland": self.locale.greenland,
                               "brazil_east": self.locale.brazil_east,
                               "guyana": self.locale.guyana,
                               "mid_atlantic": self.locale.mid_atlantic,
                               "azores": self.locale.azores,
                               "gambia": self.locale.gambia,
                               "england": self.locale.england,
                               "tunisia": self.locale.tunisia,
                               "france": self.locale.france,
                               "south_africa": self.locale.south_africa,
                               "greece": self.locale.greece,
                               "iraq": self.locale.iraq,
                               "finland": self.locale.finland,
                               "armenia": self.locale.armenia,
                               "pakistan": self.locale.pakistan,
                               "bombay": self.locale.bombay,
                               "bangladesh": self.locale.bangladesh,
                               "thailand": self.locale.thailand,
                               "china": self.locale.china,
                               "japan": self.locale.japan,
                               "south_australia": self.locale.south_australia,
                               "guam": self.locale.guam,
                               "australia": self.locale.australia,
                               "solomon_islands": self.locale.solomon_islands,
                               "fiji": self.locale.fiji,
                               "new_zealand": self.locale.new_zealand
                           }}),
            ('enable_ntp_server', {'locator': {'default': self.page.locator('#systemClock_enabled')},
                                   'type': 'switch_button'}),
            ('ntp_server_1', {'locator': {'default': self.page.locator('#systemClock_address1')}, 'type': 'fill'}),
            ('ntp_server_1_port', {'locator': {'default': self.page.locator('#systemClock_port1')}, 'type': 'fill'}),
            ('ntp_server_2', {'locator': {'default': self.page.locator('#systemClock_address2')}, 'type': 'fill'}),
            ('ntp_server_2_port', {'locator': {'default': self.page.locator('#systemClock_port2')}, 'type': 'fill'}),
            ('save', {'locator': {'default': self.page.locator('//button[@class="ant-btn ant-btn-primary"]')},
                      'type': 'button'}),
            ('text_messages', {'type': 'text_messages'}),
            ('tip_messages', {'type': 'tip_messages'}),
            ('reset', {'locator': {'default': self.page.locator('//button[@class="ant-btn ant-btn-default"]')},
                       'type': 'button', "always_do": True}),
        ]

    @property
    @AdaptModelLocator.adapt_model
    def device_options(self) -> list:
        return [
            ('device_options', {'locator': {'default': self.locale.device_options}, 'type': 'expand'}),
            ('reboot', {'locator': {'default': self.page.locator(f'button:has-text("{self.locale.reboot}")')},
                        'type': 'button'}),
            ('ok', {'locator': {'default': self.pop_up.locator('//button[@class="ant-btn ant-btn-primary"]')},
                    'type': 'button'}),
            ('cancel', {'locator': {'default': self.pop_up.locator('//button[@class="ant-btn ant-btn-default"]')},
                        'type': 'button'}),
            ('upgrade', {'locator': {'default': self.page.locator(f'button:has-text("{self.locale.upgrade}")')},
                         'type': 'upload_file'}),
            ('restore_to_factory',
             {'locator': {'default': self.page.locator(f'button:has-text("{self.locale.restore_to_factory}")')},
              'type': 'button'}),
            ('save', {'locator': {'default': self.page.locator('//button[@class="ant-btn ant-btn-primary"]')},
                      'type': 'button'}),
            ('text_messages', {'type': 'text_messages'}),
            ('tip_messages', {'type': 'tip_messages'}),
            ('reset', {'locator': {'default': self.page.locator('//button[@class="ant-btn ant-btn-default"]')},
                       'type': 'button', "always_do": True}),
        ]

    @property
    @AdaptModelLocator.adapt_model
    def configuration_management(self) -> list:
        return [
            ('configuration_management',
             {'locator': {'default': self.locale.configuration_management}, 'type': 'expand'}),
            ('export', {'locator': {'default': self.page.locator(f'button:has-text("{self.locale.config_export}")')},
                        'type': 'download_file'}),
            ('import', {'locator': {'default': self.page.locator(f'button:has-text("{self.locale.config_import}")')},
                        'type': 'upload_file'}),
            ('ok', {'locator': {'default': self.pop_up.locator('//button[@class="ant-btn ant-btn-primary"]')},
                    'type': 'button'}),
            ('cancel', {'locator': {'default': self.pop_up.locator('//button[@class="ant-btn ant-btn-default"]')},
                        'type': 'button'}),
            ('save', {'locator': {'default': self.page.locator('//button[@class="ant-btn ant-btn-primary"]')},
                      'type': 'button'}),
            ('text_messages', {'type': 'text_messages'}),
            ('tip_messages', {'type': 'tip_messages'}),
        ]

    @property
    @AdaptModelLocator.adapt_model
    def device_alarms(self) -> list:
        return [
            ('device_alarms', {'locator': {
                'default': self.page.locator(f'div:has-text("{self.locale.device_alarms}")')}, 'type': 'button'}),
            ('select_all', {'locator': {'default': self.page.locator(f'span:has-text("{self.locale.select_all}")')},
                            'type': 'check'}),
            ('user_login_success',
             {'locator': {'default': self.page.locator(f'span:has-text("{self.locale.user_login_success}")')},
              'type': 'check'}),
            ('user_login_fail',
             {'locator': {'default': self.page.locator(f'span:has-text("{self.locale.user_login_fail}")')},
              'type': 'check'}),
            ('configuration_change',
             {'locator': {'default': self.page.locator(f'span:has-text("{self.locale.configuration_change}")')},
              'type': 'check'}),
            ('cpu_too_high',
             {'locator': {'default': self.page.locator(f'span:has-text("{self.locale.cpu_too_high}")')},
              'type': 'check'}),
            ('cpu_height_setting', {'locator': {'default': self.page.locator('#rc_select_18')}, 'type': 'select'}),
            ('memory_too_high',
             {'locator': {'default': self.page.locator(f'span:has-text("{self.locale.memory_too_high}")')},
              'type': 'check'}),
            ('memory_height_setting', {'locator': {'default': self.page.locator('#rc_select_19')}, 'type': 'select'}),
            ('detection_status_change',
             {'locator': {'default': self.page.locator(f'span:has-text("{self.locale.detection_status_change}")')},
              'type': 'check'}),
            ('vpn_status_change',
             {'locator': {'default': self.page.locator(f'span:has-text("{self.locale.vpn_status_change}")')},
              'type': 'check'}),
            ('uplink_status_change',
             {'locator': {'default': self.page.locator(f'span:has-text("{self.locale.uplink_status_change}")')},
              'type': 'check'}),
            ('failover_occurs',
             {'locator': {'default': self.page.locator(f'span:has-text("{self.locale.failover_occurs}")')},
              'type': 'check'}),
            ('reboot', {'locator': {'default': self.page.locator(f'span:has-text("{self.locale.reboot_alarm}")')},
                        'type': 'check'}),
            ('upgrade', {'locator': {'default': self.page.locator(f'span:has-text("{self.locale.upgrade_alarm}")')},
                         'type': 'check'}),
            ('alarm_select_save', {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]').nth(0),
                                   'type': 'button'}),
            ('alarm_select_reset',
             {'locator': {'default': self.page.locator('//button[@class="ant-btn ant-btn-default"]').nth(0)},
              'type': 'button', "always_do": True}),
            ('enable_receive_email_settings', {'locator': {'default': self.page.locator('#sender_enable')},
                                               'type': 'switch_button'}),
            ('mail_server_address', {'locator': {'default': self.page.locator('#sender_server')}, 'type': 'fill'}),
            ('mail_server_port', {'locator': {'default': self.page.locator('#sender_port')}, 'type': 'fill'}),
            ('username', {'locator': {'default': self.page.locator('#sender_username')}, 'type': 'fill'}),
            ('password', {'locator': {'default': self.page.locator('#sender_password')}, 'type': 'fill'}),
            ('tls', {'locator': {'default': self.page.locator('#sender_tls')}, 'type': 'check'}),
            ('receiving_email_address', {'locator': {'default': self.page.locator('#receiver_0')},
                                         'type': 'multi_fill'}),
            ('send_a_test_email_to', {'locator': {'default': self.page.locator('#email')}, 'type': 'fill'}),
            ('send', {'locator': {
                'default': self.page.locator('//button[@class="ant-btn ant-btn-primary ant-input-search-button"]')},
                'type': 'button'}),
            ('alarm_mail_save', {'locator': {'default': self.page.locator(
                '//button[@class="ant-btn ant-btn-primary"]').nth(-1)}, 'type': 'button'}),
            ('alarm_mail_reset',
             {'locator': {'default': self.page.locator('//button[@class="ant-btn ant-btn-default"]').nth(-1)},
              'type': 'button', "always_do": True}),
            ('return_', {'locator': {'default': self.page.locator('.ant-page-header-back')}, 'type': 'button',
                         "always_do": True}),
            ('text_messages', {'type': 'text_messages'}),
            ('tip_messages', {'type': 'tip_messages'}),
        ]

    @property
    @AdaptModelLocator.adapt_model
    def tools(self) -> list:
        return [
            ('tools', {'locator': {'default': self.page.locator(f'div:has-text("{self.locale.tools}")')},
                       'type': 'button'}),
            ('ping_target', {'locator': {'default': self.page.locator('#pingForm_host')}, 'type': 'fill'}),
            ('ping_interface', {'locator': {'default': self.page.locator('#pingForm_interface')}, 'type': 'select'}),
            ('ping_source', {'locator': {'default': self.page.locator('#pingForm_source')}, 'type': 'fill'}),
            ('paket_size', {'locator': {'default': self.page.locator('#pingForm_packet_size')}, 'type': 'fill'}),
            ('paket_number', {'locator': {'default': self.page.locator('#pingForm_ping_count')}, 'type': 'fill'}),
            ('start_ping', {'locator': {
                'default': self.page.locator('div:has-text("Ping") >> //button[@class="ant-btn ant-btn-primary"]').nth(
                    0)}, 'type': 'button'}),
            ('stop_ping', {'locator': {
                'default': self.page.locator('div:has-text("Ping") >> //button[@class="ant-btn ant-btn-primary"]').nth(
                    0)}, 'type': 'button'}),
            ('clear_ping', {'locator': {
                'default': self.page.locator('div:has-text("Ping") >> //button[@class="ant-btn ant-btn-default"]').nth(
                    0)}, 'type': 'button'}),
            ('traceroute_target', {'locator': {'default': self.page.locator('#tracerouteForm_host')}, 'type': 'fill'}),
            ('traceroute_interface',
             {'locator': {'default': self.page.locator('#tracerouteForm_interface')}, 'type': 'select'}),
            ('start_traceroute', {'locator': {
                'default': self.page.locator(
                    'div:has-text("Traceroute") >> //button[@class="ant-btn ant-btn-primary"]').nth(0)},
                'type': 'button'}),
            ('stop_traceroute', {'locator': {
                'default': self.page.locator(
                    'div:has-text("Traceroute") >> //button[@class="ant-btn ant-btn-primary"]').nth(0)},
                'type': 'button'}),
            ('capture_interface', {'locator': {'default': self.page.locator('#captureForm_interface')},
                                   'type': 'select'}),
            ('filter_expression', {'locator': {'default': self.page.locator('#captureForm_expert_options')},
                                   'type': 'fill'}),
            ('capture_time', {'locator': {'default': self.page.locator('#captureForm_capture_time')}, 'type': 'fill'}),
            ('capture_output', {'locator': {'default': self.page.locator('#captureForm_capture_mode')},
                                'type': 'select', 'param': {'view_output_below': self.locale.view_output_below,
                                                            'export': self.locale.output_export}}),
            ('start_capture', {'locator': {
                'default': self.page.locator(
                    f'div:has-text("{self.locale.capture}") >> //button[@class="ant-btn ant-btn-primary"]').nth(0)},
                'type': 'button'}),
            ('stop_capture', {'locator': {
                'default': self.page.locator(
                    f'div:has-text("{self.locale.capture}") >> //button[@class="ant-btn ant-btn-primary"]').nth(0)},
                'type': 'button'}),
            ('clear_capture', {'locator': {
                'default': self.page.locator(
                    f'div:has-text("{self.locale.capture}") >> //button[@class="ant-btn ant-btn-default"]').nth(0)},
                'type': 'button'}),
            ('iperf_role', {'locator': {'default': self.page.locator('#role')}, 'type': 'select',
                            'param': {'server': self.locale.server, 'client': self.locale.client}}),
            ('iperf_time', {'locator': {'default': self.page.locator('#capture_time')}, 'type': 'fill'}),
            ('start_iperf', {'locator': {
                'default': self.page.locator('div:has-text("Iperf") >> //button[@class="ant-btn ant-btn-primary"]').nth(
                    0)}, 'type': 'button'}),
            ('stop_iperf', {'locator': {
                'default': self.page.locator('div:has-text("Iperf") >> //button[@class="ant-btn ant-btn-primary"]').nth(
                    0)}, 'type': 'button'}),
            ('clear_iperf', {'locator': {
                'default': self.page.locator('div:has-text("Iperf") >> //button[@class="ant-btn ant-btn-default"]').nth(
                    0)}, 'type': 'button'}),
            ('return_', {'locator': {'default': self.page.locator('.ant-page-header-back')}, 'type': 'button',
                         "always_do": True}),
            ('text_messages', {'type': 'text_messages'}),
            ('tip_messages', {'type': 'tip_messages'}),
        ]

    @property
    @AdaptModelLocator.adapt_model
    def scheduled_reboot(self) -> list:
        return [
            ('scheduled_reboot', {'locator': {'default': self.locale.scheduled_reboot}, 'type': 'expand'}),
            ('scheduled_reboot_type', {'locator': {'default': self.page.locator('#scheduleRebootForm_type')},
                                       'type': 'select',
                                       'param': {'daily': self.locale.daily, 'weekly': self.locale.weekly,
                                                 'monthly': self.locale.monthly, 'never': self.locale.never}}),
            ('start_time_click', {'locator': {'default': self.page.locator('#scheduleRebootForm_time')},
                                  'type': 'button'}),
            ('start_time', {'locator': {'default': self.page.locator('#scheduleRebootForm_time')}, 'type': 'fill'}),
            ('now', {'locator': {'default': self.page.locator(f'a:has-text("{self.locale.get("now")}")')},
                     'type': 'button'}),
            ('ok', {'locator': {'default': self.page.locator(f'a:has-text("{self.locale.get("ok")}")')},
                    'type': 'button'}),
            ('mon', {'locator': {'default': self.page.locator('.ant-tag ant-tag-checkable').nth(0)},
                     'type': 'check'}),
            ('tue', {'locator': {'default': self.page.locator('.ant-tag ant-tag-checkable').nth(1)},
                     'type': 'check'}),
            ('wed', {'locator': {'default': self.page.locator('.ant-tag ant-tag-checkable').nth(2)},
                     'type': 'check'}),
            ('thu', {'locator': {'default': self.page.locator('.ant-tag ant-tag-checkable').nth(3)},
                     'type': 'check'}),
            ('fri', {'locator': {'default': self.page.locator('.ant-tag ant-tag-checkable').nth(4)},
                     'type': 'check'}),
            ('sat', {'locator': {'default': self.page.locator('.ant-tag ant-tag-checkable').nth(5)},
                     'type': 'check'}),
            ('sun', {'locator': {'default': self.page.locator('.ant-tag ant-tag-checkable').nth(6)},
                     'type': 'check'}),
            ('reboot_date', {'locator': {'default': self.page.locator('#scheduleRebootForm_date')}, 'type': 'select'}),
            ('save', {'locator': {'default': self.page.locator('//button[@class="ant-btn ant-btn-primary"]')},
                      'type': 'button'}),
            ('text_messages', {'type': 'text_messages'}),
            ('tip_messages', {'type': 'tip_messages'}),
            ('reset', {'locator': {'default': self.page.locator('//button[@class="ant-btn ant-btn-default"]')},
                       'type': 'button', "always_do": True}),
        ]

    @property
    @AdaptModelLocator.adapt_model
    def log_server(self) -> list:
        return [
            ('log_server', {'locator': {'default': self.locale.log_server}, 'type': 'expand'}),
            ('enable_log_server', {'locator': {'default': self.page.locator('#logServer_enabled')},
                                   'type': 'switch_button'}),
            ('server_address1', {'locator': {'default': self.page.locator('#logServer_address1')}, 'type': 'fill'}),
            ('port1', {'locator': {'default': self.page.locator('#logServer_port1')}, 'type': 'fill'}),
            ('server_address2', {'locator': {'default': self.page.locator('#logServer_address2')}, 'type': 'fill'}),
            ('port2', {'locator': {'default': self.page.locator('#logServer_port2')}, 'type': 'fill'}),
            ('save', {'locator': {'default': self.page.locator('//button[@class="ant-btn ant-btn-primary"]')},
                      'type': 'button'}),
            ('text_messages', {'type': 'text_messages'}),
            ('tip_messages', {'type': 'tip_messages'}),
            ('reset', {'locator': {'default': self.page.locator('//button[@class="ant-btn ant-btn-default"]')},
                       'type': 'button', "always_do": True}),
        ]

    @property
    @AdaptModelLocator.adapt_model
    def account_management(self) -> list:
        return [
            ('account_management', {'locator': {'default': self.locale.account_management}, 'type': 'expand'}),
            ('username', {'locator': {'default': self.page.locator('#otherSettings_adm_user')}, 'type': 'fill'}),
            ('password', {'locator': {'default': self.page.locator('#otherSettings_new_psw')}, 'type': 'fill'}),
            ('confirm_password',
             {'locator': {'default': self.page.locator('#otherSettings_confirm_psw')}, 'type': 'fill'}),
            ('save', {'locator': {'default': self.page.locator('//button[@class="ant-btn ant-btn-primary"]')},
                      'type': 'button'}),
            ('text_messages', {'type': 'text_messages'}),
            ('tip_messages', {'type': 'tip_messages'}),
            ('reset', {'locator': {'default': self.page.locator('//button[@class="ant-btn ant-btn-default"]')},
                       'type': 'button', "always_do": True}),
        ]

    @property
    @AdaptModelLocator.adapt_model
    def other_settings(self) -> list:
        return [
            ('other_settings', {'locator': {'default': self.locale.other_settings}, 'type': 'expand'}),
            ('logout_timeout', {'locator': {'default': self.page.locator('#otherSettings_web_timeout')},
                                'type': 'fill'}),
            ('logout_timeout_save', {'locator': {'default': self.page.locator(
                '#otherSettings_web_timeout >> //button[@class="ant-btn ant-btn-primary"]').nth(0)}, 'type': 'button'}),
            ('logout_timeout_reset', {'locator': {'default': self.page.locator(
                '#otherSettings_web_timeout >> //button[@class="ant-btn ant-btn-default"]').nth(0)}, 'type': 'button'}),
            ('accelerated_forwarding',
             {'locator': {'default': self.page.locator('#acceleratedForwardingForm_sfe_enabled')},
              'type': 'switch_button'}),
            ('accelerated_forwarding_save', {'locator': {'default': self.page.locator(
                '#acceleratedForwardingForm_sfe_enabled >> //button[@class="ant-btn ant-btn-primary"]').nth(0)},
                                             'type': 'button'}),
            ('accelerated_forwarding_reset', {'locator': {'default': self.page.locator(
                '#acceleratedForwardingForm_sfe_enabled >> //button[@class="ant-btn ant-btn-default"]').nth(0)},
                                              'type': 'button'}),  # 不做 always_do, button不一定存在
            ('automatically_restarts', {'locator': {'default': self.page.locator('#autoRebootForm_reboot_enabled')},
                                        'type': 'switch_button'}),
            ('automatically_restarts_save', {'locator': {'default': self.page.locator(
                '#autoRebootForm_reboot_enabled >> //button[@class="ant-btn ant-btn-primary"]').nth(0)},
                                             'type': 'button'}),
            ('automatically_restarts_reset', {'locator': {'default': self.page.locator(
                '#autoRebootForm_reboot_enabled >> //button[@class="ant-btn ant-btn-default"]').nth(0)},
                                              'type': 'button'}),  # 不做 always_do, button不一定存在
            ('sip_alg', {'locator': {'default': self.page.locator('#autoRebootForm_sip_alg')},
                         'type': 'switch_button'}),
            ('sip_alg_save', {'locator': {'default': self.page.locator(
                '#autoRebootForm_sip_alg >> //button[@class="ant-btn ant-btn-primary"]').nth(0)},
                              'type': 'button'}),
            ('sip_alg_reset', {'locator': {'default': self.page.locator(
                '#autoRebootForm_sip_alg >> //button[@class="ant-btn ant-btn-default"]').nth(0)},
                               'type': 'button'}),  # 不做 always_do, button不一定存在
            ('text_messages', {'type': 'text_messages'}),
            ('tip_messages', {'type': 'tip_messages'}),
        ]

    @property
    @AdaptModelLocator.adapt_model
    def ssids(self) -> list:
        return [
            ('ssids',
             {'grid': [
                 ('add', {'locator': {'default': self.page.locator('.anticon anticon-plus').first},
                          'type': 'button'}),
                 ('ssid', {'locator': {'default': self.page.locator('#ssid')}, 'type': 'fill'}),
                 ('status', {'locator': {'default': self.page.locator('#enabled')}, 'type': 'switch_button'}),
                 ('band_24g', {'locator': {'default': self.page.locator(':nth-match(input[type="radio"], 1)')},
                               'type': 'radio'}),
                 ('band_5g', {'locator': {'default': self.page.locator(':nth-match(input[type="radio"], 2)')},
                              'type': 'radio'}),
                 ('security', {'locator': {'default': self.page.locator('#auth')}, 'type': 'select',
                               'param': {'wpa': 'WPA', 'wpa2': 'WPA2', 'open': 'OPEN', 'wpa-psk': 'WPA-PSK',
                                         'wpa2-psk': 'WPA2-PSK', 'wpa-psk/wpa2-psk': 'WPA-PSK/WPA2-PSK'}}),
                 ('encryption', {'locator': {'default': self.page.locator('#encrypt')},
                                 'type': 'select', 'param': {'ccmp': 'CCMP', 'ccmp/tkip': 'CCMP/TKIP'}}),
                 ('password', {'locator': {'default': self.page.locator('#key')}, 'type': 'fill'}),
                 ('network', {'locator': {'default': self.page.locator('#vlan')}, 'type': 'select',
                              'param': {'default': 'Default'}}),
                 ('channel', {'locator': {'default': self.page.locator('#channel')}, 'type': 'select',
                              'param': {'auto': self.locale.auto}}),
                 ('bandwidth', {'locator': {'default': self.page.locator('#bandwidth')}, 'type': 'select',
                                'param': {'20': '20MHZ', '40': '40Mhz', '80': '80Mhz'}}),
                 ('user_isolation', {'locator': {'default': self.page.locator('#ap_isolate')}, 'type': 'check'}),
                 ('hide_ssid', {'locator': {'default': self.page.locator('#hidden')}, 'type': 'check'}),
                 ('save', {'locator': self.pop_up.locator(
                     '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button',
                     'wait_for': {'type': 'hidden', 'locator': self.pop_up, 'timeout': 300 * 1000}}),
                 ('text_messages', {'type': 'text_messages'}),
                 ('tip_messages', {'type': 'tip_messages'}),
                 ('cancel',
                  {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-default"]'), 'type': 'button'}),

                 ('action_confirm', {'locator': {'default': self.page.locator('.ant-popover-inner-content').locator(
                     '.ant-btn.ant-btn-primary.ant-btn-sm.ant-btn-dangerous').first},
                                     'type': 'button'})],
                 'locator': {'default': self.page.locator('.ant-pro-grid-content-children').nth(0)},
                 'type': 'grid'})
        ]

    @property
    @AdaptModelLocator.adapt_model
    def portal(self) -> list:
        return [(
            'portal',
            {'table': [
                ('add', {'locator': {'default': self.page.locator('.anticon.anticon-plus').first},
                         'type': 'button'}),
                ('name', {'locator': {'default': self.page.locator('#portalConfigForm_name')}, 'type': 'fill'}),
                ('authentication_type', {'locator': {'default': self.page.locator('#portalConfigForm_splash_type')},
                                         'type': 'select',
                                         'param': {'click_passthrough': self.locale.click_passthrough,
                                                   'user_authentication': self.locale.user_authentication}}),
                ('target_ssid', {'locator': {'default': self.page.locator('#portalConfigForm_ssid_uuids')},
                                 'type': 'select_more'}),
                ('background_image',
                 {'locator': {'default': self.page.locator('#portalConfigForm_background_image_type')},
                  'type': 'select', 'param': {'none': self.locale.none, 'custom': self.locale.custom}}),
                ('background_image_choose_file',
                 {'locator': {'default': self.page.locator('#portalConfigForm_background_image_type_extra')},
                  'type': 'upload_file'}),
                ('logo', {'locator': {'default': self.page.locator('#portalConfigForm_logo_type')},
                          'type': 'select', 'param': {'none': self.locale.none, 'custom': self.locale.custom}}),
                ('logo_choose_file', {'locator': {'default': self.page.locator('#portalConfigForm_logo_type_extra')},
                                      'type': 'upload_file'}),
                ('splash_language', {'locator': {'default': self.page.locator('#portalConfigForm_language')},
                                     'type': 'select', 'param': {'english': 'English', 'chinese': '中文',
                                                                 'en': 'English', 'cn': '中文'}}),
                ('background_color',
                 {'locator': {'default': self.page.locator('.ant-btn.ant-btn-default.ant-btn-icon-only').nth(0)},
                  'type': 'button'}),
                ('background_color_input',
                 {'locator': {'default': self.page.locator('.ant-popover-inner >> //input[@class="ant-input"]')},
                  'type': 'fill'}),
                ('background_color_confirm',
                 {'locator': {
                     'default': self.page.locator('.ant-popover-inner >> //button[@class="ant-btn ant-btn-default"]')},
                     'type': 'button'}),
                ('title_color',
                 {'locator': {'default': self.page.locator('.ant-btn.ant-btn-default.ant-btn-icon-only').nth(1)},
                  'type': 'button'}),
                ('title_color_input',
                 {'locator': {'default': self.page.locator('.ant-popover-inner >> //input[@class="ant-input"]')},
                  'type': 'fill'}),
                ('title_color_confirm',
                 {'locator': {
                     'default': self.page.locator('.ant-popover-inner >> //button[@class="ant-btn ant-btn-default"]')},
                     'type': 'button'}),
                ('text_color',
                 {'locator': {'default': self.page.locator('.ant-btn.ant-btn-default.ant-btn-icon-only').nth(2)},
                  'type': 'button'}),
                ('text_color_input',
                 {'locator': {'default': self.page.locator('.ant-popover-inner >> //input[@class="ant-input"]')},
                  'type': 'fill'}),
                ('text_color_confirm',
                 {'locator': {
                     'default': self.page.locator('.ant-popover-inner >> //button[@class="ant-btn ant-btn-default"]')},
                     'type': 'button'}),
                ('box_color',
                 {'locator': {'default': self.page.locator('.ant-btn.ant-btn-default.ant-btn-icon-only').nth(3)},
                  'type': 'button'}),
                ('box_color_input',
                 {'locator': {'default': self.page.locator('.ant-popover-inner >> //input[@class="ant-input"]')},
                  'type': 'fill'}),
                ('box_color_confirm',
                 {'locator': {
                     'default': self.page.locator('.ant-popover-inner >> //button[@class="ant-btn ant-btn-default"]')},
                     'type': 'button'}),
                ('button_color',
                 {'locator': {'default': self.page.locator('.ant-btn.ant-btn-default.ant-btn-icon-only').nth(4)},
                  'type': 'button'}),
                ('button_color_input',
                 {'locator': {'default': self.page.locator('.ant-popover-inner >> //input[@class="ant-input"]')},
                  'type': 'fill'}),
                ('button_color_confirm',
                 {'locator': {
                     'default': self.page.locator('.ant-popover-inner >> //button[@class="ant-btn ant-btn-default"]')},
                     'type': 'button'}),
                ('title', {'locator': {'default': self.page.locator('#portalConfigForm_title')}, 'type': 'fill'}),
                ('welcome_message', {'locator': {'default': self.page.locator('#portalConfigForm_message')},
                                     'type': 'fill'}),
                ('button_text', {'locator': {'default': self.page.locator('#portalConfigForm_button_content')},
                                 'type': 'fill'}),
                ('box_opacity', {'locator': {'default': self.page.locator('#portalConfigForm_box_transparency')},
                                 'type': 'fill'}),
                ('next_behavior', {'locator': {'default': self.page.locator('#portalConfigForm_action')},
                                   'type': 'select',
                                   'param': {'stay_on_the_splash_page': self.locale.stay_on_the_splash_page,
                                             'redirect_url': self.locale.redirect_url}}),
                ('save', {'locator': {'default': self.page.locator('//button[@class="ant-btn ant-btn-primary"]')},
                          'type': 'button',
                          'wait_for': {'type': 'hidden', 'locator': self.pop_up, 'timeout': 300 * 1000}}),
                ('text_messages', {'type': 'text_messages'}),
                ('tip_messages', {'type': 'tip_messages'}),
                ('cancel',
                 {'locator': self.page.locator('//button[@class="ant-btn ant-btn-default"]'), 'type': 'button',
                  "always_do": True}),
                ('action_confirm', {'locator': {'default': self.page.locator('.ant-popover-inner-content').locator(
                    '.ant-btn.ant-btn-primary.ant-btn-sm.ant-btn-dangerous').first},
                                    'type': 'button'})],
                'locator': {'default': self.page.locator('.ant-table-container').nth(0)
                            },
                'type': 'table_tr'})
        ]

    @property
    @AdaptModelLocator.adapt_model
    def clients(self) -> list:
        return [
            ('all', {'locator': {'default': self.page.locator('.ant-radio-button-input').nth(0)}, 'type': 'radio'}),
            ('wired', {'locator': {'default': self.page.locator('.ant-radio-button-input').nth(1)}, 'type': 'radio'}),
            ('wireless',
             {'locator': {'default': self.page.locator('.ant-radio-button-input').nth(2)}, 'type': 'radio'}),
            ('filter_type',
             {'locator': {'default': self.page.locator('.ant-select-selection-search-input')}, 'type': 'select',
              'param': {'name': self.locale.name, 'mac_address': self.locale.mac_address,
                        'ip_address': self.locale.ip_address, 'vlan': 'VLAN'}}),
        ]

    @AdaptModelLocator.adapt_model
    def clients_status(self, ip) -> list:
        ip_address = f'//td[text()="{ip}"]'
        return [
            ('name',
             {'locator': {'default': self.page.locator(f'//td[text()="{ip}"]/../td[1]')}, 'type': 'title'}),
            ('exist', {'locator': {'default': self.page.locator(ip_address)}, 'type': 'text'}),
            ('uplink_interface', {'locator': {
                'default': self.page.locator(f'//td[text()="{ip}"]/../td[3]')}, 'type': 'text'}),
            ('vlan', {'locator': {
                'default': self.page.locator(f'//td[text()="{ip}"]/../td[4]')}, 'type': 'text'}),
            ('connection', {'locator': {
                'default': self.page.locator(f'//td[text()="{ip}"]/../td[5]')}, 'type': 'text'}),
            ('traffic', {'locator': {
                'default': self.page.locator(f'//td[text()="{ip}"]/../td[6]')}, 'type': 'text', 'split': ' ',
                'index': 0}),
            ('traffic_unit', {'locator': {
                'default': self.page.locator(f'//td[text()="{ip}"]/../td[6]')}, 'type': 'text', 'split': ' ',
                'index': 1}),
            ('up', {'locator': {
                'default': self.page.locator(f'//td[text()="{ip}"]/../td[7]')}, 'type': 'text', 'split': ' ',
                'index': 0}),
            ('up_unit', {'locator': {
                'default': self.page.locator(f'//td[text()="{ip}"]/../td[7]')}, 'type': 'text', 'split': ' ',
                'index': 1}),
            ('down', {'locator': {
                'default': self.page.locator(f'//td[text()="{ip}"]/../td[8]')}, 'type': 'text', 'split': ' ',
                'index': 0}),
            ('down_unit', {'locator': {
                'default': self.page.locator(f'//td[text()="{ip}"]/../td[8]')}, 'type': 'text', 'split': ' ',
                'index': 1}),
            ('uptime', {'locator': {
                'default': self.page.locator(f'//td[text()="{ip}"]/../td[9]')}, 'type': 'text'}),
        ]

    @AdaptModelLocator.adapt_model
    def ipsec_status(self, name) -> list:
        ipsec_name = f'//td[@class="ant-table-cell"]//div[text()="{name}"]'
        return [
            ('status',
             {'locator': {'default': self.page.locator(f'{ipsec_name}/../../../td[1]/span')}, 'type': 'style',
              'param': {'up': 'rgb(66, 182, 81)', 'down': 'rgb(216, 216, 216)'}}),
            ('exist', {'locator': {
                'default': self.page.locator(ipsec_name)}, 'type': 'text'}),
            ('uplink_interface', {'locator': {
                'default': self.page.locator(f'{ipsec_name}/../../../td[3]')}, 'type': 'text'}),
            ('interface_address',
             {'locator': {'default': self.page.locator(f'{ipsec_name}/../../../td[4]')}, 'type': 'text'}),
            ('remote_address',
             {'locator': {'default': self.page.locator(f'{ipsec_name}/../../../td[5]')}, 'type': 'text'}),
            ('available_subnets',
             {'locator': {'default': self.page.locator(f'{ipsec_name}/../../../td[6]')}, 'type': 'text'}),
            ('traffic',
             {'locator': {'default': self.page.locator(f'{ipsec_name}/../../../td[7]')}, 'type': 'text', 'split': ' ',
              'index': 0}),
            ('traffic_unit',
             {'locator': {'default': self.page.locator(f'{ipsec_name}/../../../td[7]')}, 'type': 'text', 'split': ' ',
              'index': 1}),
            ('last_connection_time',
             {'locator': {'default': self.page.locator(f'{ipsec_name}/../../../td[8]')}, 'type': 'text'}),
        ]

    @AdaptModelLocator.adapt_model
    def l2tp_status(self, name) -> list:
        l2tp_name = f'//td[text()="{name}"]'
        return [
            ('status',
             {'locator': {'default': self.page.locator(f'{l2tp_name}/../td[1]/span')}, 'type': 'style',
              'param': {'up': 'rgb(66, 182, 81)', 'down': 'rgb(216, 216, 216)'}}),
            ('exist', {'locator': {
                'default': self.page.locator(l2tp_name)}, 'type': 'text'}),
            ('type', {'locator': {
                'default': self.page.locator(f'{l2tp_name}/../td[3]')}, 'type': 'text'}),
            ('local_address',
             {'locator': {'default': self.page.locator(f'{l2tp_name}/../td[4]')}, 'type': 'text'}),
            ('peer_address',
             {'locator': {'default': self.page.locator(f'{l2tp_name}/../td[5]')}, 'type': 'text'}),
            ('traffic',
             {'locator': {'default': self.page.locator(f'{l2tp_name}/../td[6]')}, 'type': 'text', 'split': ' ',
              'index': 0}),
            ('traffic_unit',
             {'locator': {'default': self.page.locator(f'{l2tp_name}/../td[6]')}, 'type': 'text', 'split': ' ',
              'index': 1}),
            ('last_connection_time',
             {'locator': {'default': self.page.locator(f'{l2tp_name}/../td[8]')}, 'type': 'text'}),
        ]

    @AdaptModelLocator.adapt_model
    def link_health_status(self, uplink) -> list:
        uplink_name = f'//td[text()="{uplink}"]'
        return [
            ('status',
             {'locator': {'default': self.page.locator(f'{uplink_name}/../td[1]/span')}, 'type': 'class',
              'param': {'up': 'rgb(48, 161, 48)', 'down': 'rgb(220, 221, 224)', 'disable': 'rgb(193, 197, 209)',
                        'abnormal': 'rgb(246, 167, 11)'}}),
            ('exist', {'locator': {
                'default': self.page.locator(uplink_name)}, 'type': 'text'}),
            ('carrier', {'locator': {
                'default': self.page.locator(f'{uplink_name}/../td[3]/span')}, 'type': 'text'}),
            ('usage_up',
             {'locator': {'default': self.page.locator(f'{uplink_name}/../td[4]/div[1]/span[2]')}, 'type': 'text',
              'split': ' ', 'index': 0}),
            ('usage_up_unit',
             {'locator': {'default': self.page.locator(f'{uplink_name}/../td[4]/div[1]/span[2]')}, 'type': 'text',
              'split': ' ', 'index': 1}),
            ('usage_down',
             {'locator': {'default': self.page.locator(f'{uplink_name}/../td[4]/div[2]/span[2]')}, 'type': 'text',
              'split': ' ', 'index': 0}),
            ('usage_down_unit',
             {'locator': {'default': self.page.locator(f'{uplink_name}/../td[4]/div[2]/span[2]')}, 'type': 'text',
              'split': ' ', 'index': 1}),
            ('throughput_up',
             {'locator': {'default': self.page.locator(f'{uplink_name}/../td[5]/div[1]/span[2]')}, 'type': 'text',
              'split': ' ', 'index': 0}),
            ('throughput_up_unit',
             {'locator': {'default': self.page.locator(f'{uplink_name}/../td[5]/div[1]/span[2]')}, 'type': 'text',
              'split': ' ', 'index': 1}),
            ('throughput_down',
             {'locator': {'default': self.page.locator(f'{uplink_name}/../td[5]/div[2]/span[2]')}, 'type': 'text',
              'split': ' ', 'index': 0}),
            ('throughput_down_unit',
             {'locator': {'default': self.page.locator(f'{uplink_name}/../td[5]/div[2]/span[2]')}, 'type': 'text',
              'split': ' ', 'index': 1}),
            ('latency',
             {'locator': {'default': self.page.locator(f'{uplink_name}/../td[6]')}, 'type': 'text',
              'split': ' ', 'index': 0}),
            ('latency_unit',
             {'locator': {'default': self.page.locator(f'{uplink_name}/../td[6]')}, 'type': 'text',
              'split': ' ', 'index': 1}),
            ('loss',
             {'locator': {'default': self.page.locator(f'{uplink_name}/../td[7]')}, 'type': 'text'}),
            ('signal_strength',
             {'locator': {'default': self.page.locator(f'{uplink_name}/../td[8]')}, 'type': 'text'}),
        ]

    @property
    @AdaptModelLocator.adapt_model
    def passthrough_status(self) -> list:
        passthrough_div = self.page.locator('.ant-spin-container').nth(0)
        return [
            ('status',
             {'locator': {'default': passthrough_div.locator(f'//span[text()="{self.locale.status}"]/../span[2]')},
              'type': 'text', }),
            ('passthrough_wan', {'locator': {
                'default': self.page.locator('//span[text()="Passthrough WAN"]/../span[2]')}, 'type': 'text'}),
            ('passthrough_lan', {'locator': {
                'default': self.page.locator(f'//span[text()="Passthrough LAN"]/../span[2]')}, 'type': 'text'}),
            ('passthrough_ip_mask',
             {'locator': {
                 'default': self.page.locator(f'//span[text()="{self.locale.passthrough_ip_mask}"]/../span[2]')},
                 'type': 'text'}),
            ('passthrough_gateway',
             {'locator': {
                 'default': self.page.locator(f'//span[text()="{self.locale.passthrough_gateway}"]/../span[2]')},
                 'type': 'text'}),
            ('passthrough_dns1',
             {'locator': {
                 'default': self.page.locator('//span[text()="Passthrough DNS1"]/../span[2]')}, 'type': 'text'}),
            ('passthrough_dns2',
             {'locator': {
                 'default': self.page.locator('//span[text()="Passthrough DNS2"]/../span[2]')}, 'type': 'text'}),
            ('passthrough_mac',
             {'locator': {
                 'default': self.page.locator('//span[text()="Passthrough MAC"]/../span[2]')}, 'type': 'text'}),
            ('address_allocation_status',
             {'locator': {
                 'default': self.page.locator(f'//span[text()="{self.locale.address_allocation_status}"]/../span[2]')},
                 'type': 'text'}),
            ('lease_timeout',
             {'locator': {
                 'default': self.page.locator(f'//span[text()="{self.locale.lease_timeout}"]/../span[2]')},
                 'type': 'text'}),
        ]

    @property
    @AdaptModelLocator.adapt_model
    def wan(self) -> list:
        return [
            ('type_', {'locator': {'default': self.page.locator('#ipType')}, 'type': 'select',
                       'param': {'static_ip': self.locale.static_ip, 'dhcp': 'DHCP'}}),
            ('ip_address', {'locator': {'default': self.page.locator('#ip')}, 'type': 'fill'}),
            ('mask', {'locator': {'default': self.page.locator('#mask')}, 'type': 'fill'}),
            ('gateway_address', {'locator': {'default': self.page.locator('#gateway')}, 'type': 'fill'}),
            ('main_dns', {'locator': {'default': self.page.locator('#dns1')}, 'type': 'fill'}),
            ('secondary_dns', {'locator': {'default': self.page.locator('#dns2')}, 'type': 'fill'}),
            ('mtu', {'locator': {'default': self.page.locator('#mtu')}, 'type': 'fill'}),
            ('save', {'locator': {'default': self.page.locator('//button[@class="ant-btn ant-btn-primary"]')},
                      'type': 'button'}),
            ('text_messages', {'type': 'text_messages'}),
            ('tip_messages', {'type': 'tip_messages'}),
            ('reset', {'locator': {'default': self.page.locator('//button[@class="ant-btn ant-btn-default"]')},
                       'type': 'button', "always_do": True}),
        ]

    @property
    @AdaptModelLocator.adapt_model
    def interface_status(self) -> list:
        # dashboard 页面中间接口
        lan1_center = self.page.locator('//div[@style="text-align: center;"]').locator('div:has-text("LAN1")').locator(
            '..')
        lan2_center = self.page.locator('//div[@style="text-align: center;"]').locator('div:has-text("LAN2")').locator(
            '..')
        lan3_center = self.page.locator('//div[@style="text-align: center;"]').locator('div:has-text("LAN3")').locator(
            '..')
        lan4_center = self.page.locator('//div[@style="text-align: center;"]').locator('div:has-text("LAN4")').locator(
            '..')
        lan5_center = self.page.locator('//div[@style="text-align: center;"]').locator('div:has-text("LAN5")').locator(
            '..')
        wan1_center = self.page.locator('//div[@style="text-align: center;"]').locator('div:has-text("WAN1")').locator(
            '..')
        wan2_center = self.page.locator('//div[@style="text-align: center;"]').locator('div:has-text("WAN2")').locator(
            '..')
        cellular_center = self.page.locator('//div[@style="text-align: center;"]').locator(
            'div:has-text("Cellular")').locator('..')
        wifi_sta_center = self.page.locator('//div[@style="text-align: center;"]').locator(
            'div:has-text("Wi-Fi(STA)")').locator('..')
        drawer_content_wrapper = self.page.locator('//div[@class="ant-drawer-content-wrapper"]')
        # 右侧展开栏
        lan1 = drawer_content_wrapper.locator('.ant-collapse-header', has=self.page.locator(
            'span:has-text("LAN1")')).locator('..')
        lan2 = drawer_content_wrapper.locator('.ant-collapse-header', has=self.page.locator(
            'span:has-text("LAN2")')).locator('..')
        lan3 = drawer_content_wrapper.locator('.ant-collapse-header', has=self.page.locator(
            'span:has-text("LAN3")')).locator('..')
        lan4 = drawer_content_wrapper.locator('.ant-collapse-header', has=self.page.locator(
            'span:has-text("LAN4")')).locator('..')
        lan5 = drawer_content_wrapper.locator('.ant-collapse-header', has=self.page.locator(
            'span:has-text("LAN5")')).locator('..')
        wan1 = drawer_content_wrapper.locator('.ant-collapse-header',
                                              has=self.page.locator('span:has-text("WAN1")')).locator('..')
        wan2 = drawer_content_wrapper.locator('.ant-collapse-header',
                                              has=self.page.locator('span:has-text("WAN2")')).locator('..')
        cellular = drawer_content_wrapper.locator('.ant-collapse-header',
                                                  has=self.page.locator('span:has-text("Cellular")')).locator('..')
        wifi_sta = drawer_content_wrapper.locator('.ant-collapse-header',
                                                  has=self.page.locator('span:has-text("Wi-Fi(STA)")')).locator('..')
        return [
            ('lan1', {'locator': {'default': lan1_center}, 'type': 'button', 'wait_for': {
                'type': 'visible', 'locator': drawer_content_wrapper, 'timeout': 300 * 1000}}),
            ('lan2', {'locator': {'default': lan2_center}, 'type': 'button', 'wait_for': {
                'type': 'visible', 'locator': drawer_content_wrapper, 'timeout': 300 * 1000}}),
            ('lan3', {'locator': {'default': lan3_center}, 'type': 'button', 'wait_for': {
                'type': 'visible', 'locator': drawer_content_wrapper, 'timeout': 300 * 1000}}),
            ('lan4', {'locator': {'default': lan4_center}, 'type': 'button', 'wait_for': {
                'type': 'visible', 'locator': drawer_content_wrapper, 'timeout': 300 * 1000}}),
            ('lan5', {'locator': {'default': lan5_center}, 'type': 'button', 'wait_for': {
                'type': 'visible', 'locator': drawer_content_wrapper, 'timeout': 300 * 1000}}),
            ('wan1', {'locator': {'default': wan1_center}, 'type': 'button', 'wait_for': {
                'type': 'visible', 'locator': drawer_content_wrapper, 'timeout': 300 * 1000}}),
            ('wan2', {'locator': {'default': wan2_center}, 'type': 'button', 'wait_for': {
                'type': 'visible', 'locator': drawer_content_wrapper, 'timeout': 300 * 1000}}),
            ('cellular', {'locator': {'default': cellular_center}, 'type': 'button',
                          'wait_for': {'type': 'visible', 'locator': drawer_content_wrapper, 'timeout': 300 * 1000}}),
            ('wifi_sta', {'locator': {'default': wifi_sta_center}, 'type': 'button',
                          'wait_for': {'type': 'visible', 'locator': drawer_content_wrapper, 'timeout': 300 * 1000}}),
            ('lan1_expand', {'locator': {'default': 'LAN1'}, 'type': 'expand'}),
            ('lan2_expand', {'locator': {'default': 'LAN2'}, 'type': 'expand'}),
            ('lan3_expand', {'locator': {'default': 'LAN3'}, 'type': 'expand'}),
            ('lan4_expand', {'locator': {'default': 'LAN4'}, 'type': 'expand'}),
            ('lan5_expand', {'locator': {'default': 'LAN5'}, 'type': 'expand'}),
            ('wan1_expand', {'locator': {'default': 'WAN1'}, 'type': 'expand'}),
            ('wan2_expand', {'locator': {'default': 'WAN2'}, 'type': 'expand'}),
            ('cellular_expand', {'locator': {'default': 'Cellular'}, 'type': 'expand'}),
            ('wifi_sta_expand', {'locator': {'default': 'Wi-Fi(STA)'}, 'type': 'expand'}),
            ('lan1_status', {"locator": lan1.locator(f'span:has-text("{self.locale.status}")').locator('..//span[2]'),
                             "type": 'text', "param": {'disconnected': self.locale.disconnect,
                                                       'connected': self.locale.connect}}),
            ('lan1_link_rate', {"locator": lan1.locator(f'span:has-text("{self.locale.link_rate}")').locator(
                '..//span[2]'), "type": 'text'}),
            ('lan1_network', {"locator": lan1.locator(f'span:has-text("{self.locale.network}")').locator('..//span[2]'),
                              "type": 'text', 'param': {'all': self.locale.all}}),
            ('lan2_status', {"locator": lan2.locator(f'span:has-text("{self.locale.status}")').locator('..//span[2]'),
                             "type": 'text', "param": {'disconnected': self.locale.disconnect,
                                                       'connected': self.locale.connect}}),
            ('lan2_link_rate', {"locator": lan2.locator(f'span:has-text("{self.locale.link_rate}")').locator(
                '..//span[2]'), "type": 'text'}),
            ('lan2_network', {"locator": lan2.locator(f'span:has-text("{self.locale.network}")').locator('..//span[2]'),
                              'type': 'text', 'param': {'all': self.locale.all}}),
            ('lan3_status', {"locator": lan3.locator(f'span:has-text("{self.locale.status}")').locator('..//span[2]'),
                             "type": 'text', "param": {'disconnected': self.locale.disconnect,
                                                       'connected': self.locale.connect}}),
            ('lan3_link_rate', {"locator": lan3.locator(f'span:has-text("{self.locale.link_rate}")').locator(
                '..//span[2]'), "type": 'text'}),
            ('lan3_network', {"locator": lan3.locator(f'span:has-text("{self.locale.network}")').locator('..//span[2]'),
                              'type': 'text', 'param': {'all': self.locale.all}}),
            ('lan4_status', {"locator": lan4.locator(f'span:has-text("{self.locale.status}")').locator('..//span[2]'),
                             "type": 'text',
                             "param": {'disconnected': self.locale.disconnect, 'connected': self.locale.connect}}),
            ('lan4_link_rate', {"locator": lan4.locator(f'span:has-text("{self.locale.link_rate}")').locator(
                '..//span[2]'), "type": 'text'}),
            ('lan4_network', {"locator": lan4.locator(f'span:has-text("{self.locale.network}")').locator('..//span[2]'),
                              'type': 'text', 'param': {'all': self.locale.all}}),
            ('lan5_status', {"locator": lan5.locator(f'span:has-text("{self.locale.status}")').locator('..//span[2]'),
                             "type": 'text', "param": {'disconnected': self.locale.disconnect,
                                                       'connected': self.locale.connect}}),
            ('lan5_link_rate', {"locator": lan5.locator(f'span:has-text("{self.locale.link_rate}")').locator(
                '..//span[2]'), "type": 'text'}),
            ('lan5_network', {"locator": lan5.locator(f'span:has-text("{self.locale.network}")').locator('..//span[2]'),
                              'type': 'text', 'param': {'all': self.locale.all}}),
            ('wan1_status', {"locator": wan1.locator(f'span:has-text("{self.locale.status}")').locator('..//span[2]'),
                             "type": 'text', "param": {'disconnected': self.locale.disconnect,
                                                       'connected': self.locale.connect}}),
            ('wan1_work_mode', {"locator": wan1.locator(f'span:has-text("{self.locale.work_mode}")').locator(
                '..//span[2]'), "type": 'text', 'param': {'active': self.locale.active}}),
            ('wan1_ipv4_type', {"locator": wan1.locator(f'span:has-text("{self.locale.ipv4_type}")').locator(
                '..//span[2]'), 'type': 'text'}),
            ('wan1_ipv4_address', {"locator": wan1.locator(f'span:has-text("{self.locale.ipv4_address}")').locator(
                '..//span[2]'), 'type': 'text'}),
            ('wan1_ipv4_gateway', {"locator": wan1.locator(f'span:has-text("{self.locale.ipv4_gateway}")').locator(
                '..//span[2]'), 'type': 'text'}),
            ('wan1_lease_acquisition_time', {"locator": wan1.locator(
                f'span:has-text("{self.locale.lease_acquisition_time}")').locator('..//span[2]'), 'type': 'text'}),
            ('wan1_lease_timeout', {"locator": wan1.locator(f'span:has-text("{self.locale.lease_timeout}")').locator(
                '..//span[2]'), 'type': 'text'}),
            ('wan1_primary_dns', {"locator": wan1.locator(f'span:has-text("{self.locale.primary_dns}")').locator(
                '..//span[2]'), 'type': 'text'}),
            ('wan1_secondary_dns', {"locator": wan1.locator(f'span:has-text("{self.locale.secondary_dns}")').locator(
                '..//span[2]'), 'type': 'text'}),
            ('wan1_ipv6_type', {"locator": wan1.locator(f'span:has-text("{self.locale.ipv6_type}")').locator(
                '..//span[2]'), 'type': 'text'}),
            ('wan1_ipv6_address', {"locator": wan1.locator(f'span:has-text("{self.locale.ipv6_address}")').locator(
                '..//span[2]'), 'type': 'text'}),
            ('wan1_ipv6_gateway', {"locator": wan1.locator(f'span:has-text("{self.locale.ipv6_gateway}")').locator(
                '..//span[2]'), 'type': 'text'}),
            ('wan1_main_ipv6_dns', {"locator": wan1.locator(f'span:has-text("{self.locale.main_ipv6_dns}")').locator(
                '..//span[2]'), 'type': 'text'}),
            ('wan1_secondary_ipv6_dns', {"locator": wan1.locator(
                f'span:has-text("{self.locale.secondary_ipv6_dns}")').locator('..//span[2]'), 'type': 'text'}),
            ('wan1_test_connectivity_to', {"locator": wan1.locator(
                f'span:has-text("{self.locale.test_connectivity_to}")').locator('..//span[2]'), 'type': 'text'}),
            ('wan2_status', {"locator": wan2.locator(f'span:has-text("{self.locale.status}")').locator('..//span[2]'),
                             "type": 'text', "param": {'disconnected': self.locale.disconnect,
                                                       'connected': self.locale.connect}}),
            ('wan2_work_mode', {"locator": wan2.locator(f'span:has-text("{self.locale.work_mode}")').locator(
                '..//span[2]'), "type": 'text', 'param': {'active': self.locale.active}}),
            ('wan2_ipv4_type', {"locator": wan2.locator(f'span:has-text("{self.locale.ipv4_type}")').locator(
                '..//span[2]'), 'type': 'text'}),
            ('wan2_ipv4_address', {"locator": wan2.locator(f'span:has-text("{self.locale.ipv4_address}")').locator(
                '..//span[2]'), 'type': 'text'}),
            ('wan2_ipv4_gateway', {"locator": wan2.locator(f'span:has-text("{self.locale.ipv4_gateway}")').locator(
                '..//span[2]'), 'type': 'text'}),
            ('wan2_lease_acquisition_time', {"locator": wan2.locator(
                f'span:has-text("{self.locale.lease_acquisition_time}")').locator('..//span[2]'), 'type': 'text'}),
            ('wan2_lease_timeout', {"locator": wan2.locator(f'span:has-text("{self.locale.lease_timeout}")').locator(
                '..//span[2]'), 'type': 'text'}),
            ('wan2_primary_dns', {"locator": wan2.locator(f'span:has-text("{self.locale.primary_dns}")').locator(
                '..//span[2]'), 'type': 'text'}),
            ('wan2_secondary_dns', {"locator": wan2.locator(f'span:has-text("{self.locale.secondary_dns}")').locator(
                '..//span[2]'), 'type': 'text'}),
            ('wan2_ipv6_type', {"locator": wan2.locator(f'span:has-text("{self.locale.ipv6_type}")').locator(
                '..//span[2]'), 'type': 'text'}),
            ('wan2_ipv6_address', {"locator": wan2.locator(f'span:has-text("{self.locale.ipv6_address}")').locator(
                '..//span[2]'), 'type': 'text'}),
            ('wan2_ipv6_gateway', {"locator": wan2.locator(f'span:has-text("{self.locale.ipv6_gateway}")').locator(
                '..//span[2]'), 'type': 'text'}),
            ('wan2_main_ipv6_dns', {"locator": wan2.locator(f'span:has-text("{self.locale.main_ipv6_dns}")').locator(
                '..//span[2]'), 'type': 'text'}),
            ('wan2_secondary_ipv6_dns', {"locator": wan2.locator(
                f'span:has-text("{self.locale.secondary_ipv6_dns}")').locator('..//span[2]'), 'type': 'text'}),
            ('wan2_test_connectivity_to', {"locator": wan2.locator(
                f'span:has-text("{self.locale.test_connectivity_to}")').locator('..//span[2]'), 'type': 'text'}),
            ('cellular_status', {"locator": cellular.locator(f'span:has-text("{self.locale.status}")').locator(
                '..//span[2]'), "type": 'text', "param": {'disconnected': self.locale.disconnect,
                                                          'connected': self.locale.connect}}),
            ('cellular_work_mode', {"locator": cellular.locator(f'span:has-text("{self.locale.work_mode}")').locator(
                '..//span[2]'), "type": 'text', 'param': {'active': self.locale.active,
                                                          'standby': self.locale.standby}}),
            ('cellular_sim', {'locator': cellular.locator('span:has-text("SIM")').locator('..//span[2]'),
                              'type': 'text'}),
            ('cellular_carrier', {'locator': cellular.locator(f'span:has-text("{self.locale.carrier}")').locator(
                '..//span[2]'), 'type': 'text'}),
            ('cellular_network_mode', {"locator": cellular.locator(
                f'span:has-text("{self.locale.network_mode}")').locator('..//span[2]'), 'type': 'text'}),
            ('cellular_apn', {"locator": cellular.locator('span:has-text("APN")').locator('..//span[2]'),
                              'type': 'text'}),
            ('cellular_ipv4_address', {"locator": cellular.locator(
                f'span:has-text("{self.locale.ipv4_address}")').locator('..//span[2]'), 'type': 'text'}),
            ('cellular_ipv4_gateway', {"locator": cellular.locator(
                f'span:has-text("{self.locale.ipv4_gateway}")').locator('..//span[2]'), 'type': 'text'}),
            ('cellular_primary_dns', {"locator": cellular.locator(
                f'span:has-text("{self.locale.primary_dns}")').locator('..//span[2]'), 'type': 'text'}),
            ('cellular_secondary_dns', {"locator": cellular.locator(
                f'span:has-text("{self.locale.secondary_dns}")').locator('..//span[2]'), 'type': 'text'}),
            ('cellular_ipv6_address',
             {"locator": cellular.locator(f'span:has-text("{self.locale.ipv6_address}")').locator('..//span[2]'),
              'type': 'text'}),
            ('cellular_ipv6_gateway',
             {"locator": cellular.locator(f'span:has-text("{self.locale.ipv6_gateway}")').locator('..//span[2]'),
              'type': 'text'}),
            ('cellular_test_connectivity_to', {"locator": cellular.locator(
                f'span:has-text("{self.locale.test_connectivity_to}")').locator('..//span[2]'), 'type': 'text'}),
            ('cellular_used_traffic_threshold', {"locator": cellular.locator(
                f'span:has-text("{self.locale.used_traffic_threshold}")').locator('..//span[2]'), 'type': 'text'}),
            ('cellular_iccid', {"locator": cellular.locator('span:has-text("ICCID")').locator('..//span[2]'),
                                'type': 'text'}),
            ('cellular_imei', {"locator": cellular.locator('span:has-text("IMEI")').locator('..//span[2]'),
                               'type': 'text'}),
            ('cellular_imsi', {"locator": cellular.locator('span:has-text("IMSI")').locator('..//span[2]'),
                               'type': 'text'}),
            ('cellular_pci', {"locator": cellular.locator('span:has-text("PCI")').locator('..//span[2]'),
                              'type': 'text'}),
            ('cellular_cell_id', {"locator": cellular.locator(f'span:has-text("{self.locale.cell_id}")').locator(
                '..//span[2]'), 'type': 'text'}),
            ('cellular_lac', {"locator": cellular.locator('span:has-text("LAC")').locator('..//span[2]'),
                              'type': 'text'}),
            ('cellular_arfcn', {"locator": cellular.locator('span:has-text("ARFCN")').locator('..//span[2]'),
                                'type': 'text'}),
            ('cellular_band', {"locator": cellular.locator('span:has-text("BAND")').locator('..//span[2]'),
                               'type': 'text'}),
            ('cellular_traffic_reset_time', {"locator": cellular.locator(
                f'span:has-text("{self.locale.traffic_reset_time}")').locator('..//span[2]'), 'type': 'text'}),
            ('cellular_connect_time', {"locator": cellular.locator(
                f'span:has-text("{self.locale.connect_time}")').locator('..//span[2]'), 'type': 'text'}),
            ('wifi_sta_status', {"locator": wifi_sta.locator(f'span:has-text("{self.locale.status}")').locator(
                '..//span[2]'), "type": 'text', "param": {'disconnected': self.locale.disconnect,
                                                          'connected': self.locale.connect}}),
            ('wifi_sta_work_mode', {"locator": wifi_sta.locator(f'span:has-text("{self.locale.work_mode}")').locator(
                '..//span[2]'), "type": 'text', 'param': {'standby': self.locale.standby}}),
            ('wifi_sta_ssid', {"locator": wifi_sta.locator('span:has-text("SSID")').locator('..//span[2]'),
                               'type': 'text'}),
            ('wifi_sta_band', {"locator": wifi_sta.locator(f'span:has-text("{self.locale.band}")').locator(
                '..//span[2]'), 'type': 'text'}),
            ('wifi_sta_type', {"locator": wifi_sta.locator(f'span:has-text("{self.locale.type_}")').locator(
                '..//span[2]'), 'type': 'text'}),
            ('wifi_sta_ip_address', {"locator": wifi_sta.locator(
                f'span:has-text("{self.locale.ip_address}")').locator('..//span[2]'), 'type': 'text'}),
            ('wifi_sta_gateway_address', {"locator": wifi_sta.locator(
                f'span:has-text("{self.locale.gateway_address}")').locator('..//span[2]'), 'type': 'text'}),
            ('wifi_sta_lease_acquisition_time', {"locator": wifi_sta.locator(
                f'span:has-text("{self.locale.lease_acquisition_time}")').locator('..//span[2]'), 'type': 'text'}),
            ('wifi_sta_lease_timeout', {"locator": wifi_sta.locator(
                f'span:has-text("{self.locale.lease_timeout}")').locator('..//span[2]'), 'type': 'text'}),
            ('wifi_sta_primary_dns', {"locator": wifi_sta.locator(
                f'span:has-text("{self.locale.primary_dns}")').locator('..//span[2]'), 'type': 'text'}),
            ('wifi_sta_secondary_dns', {"locator": wifi_sta.locator(
                f'span:has-text("{self.locale.secondary_dns}")').locator('..//span[2]'), 'type': 'text'}),
            ('wifi_sta_test_connectivity_to', {"locator": wifi_sta.locator(
                f'span:has-text("{self.locale.test_connectivity_to}")').locator('..//span[2]'), 'type': 'text'}),
            ('wifi_sta_connect_time', {"locator": wifi_sta.locator(
                f'span:has-text("{self.locale.connect_time}")').locator('..//span[2]'), 'type': 'text'}),
            ('close', {'locator': {'default': self.page.locator('.anticon.anticon-close')}, 'type': 'button',
                       'wait_for': {'type': 'timeout', 'timeout': 1000}}),
        ]

    @property
    @AdaptModelLocator.adapt_model
    def radio(self) -> list:
        return [
            ('24g_radio_channel_width_20',
             {'locator': {'default': self.page.locator('div:has-text("2.4GHz Radio")').locator('..').locator(
                 '//div[@class="ant-slider-mark"]/span[1]')}, 'type': 'button'}),
            ('24g_radio_channel_width_40',
             {'locator': {'default': self.page.locator('div:has-text("2.4GHz Radio")').locator('..').locator(
                 '//div[@class="ant-slider-mark"]/span[2]')}, 'type': 'button'}),
            ('24g_radio_transmit_power',
             {'locator': {'default': self.page.locator('#wlan1_txpower_level')}, 'type': 'select',
              'param': {'auto': self.locale.auto, 'low': self.locale.radio_low, 'medium': self.locale.medium,
                        'height': self.locale.radio_height, 'custom': self.locale.custom}}),
            ('24g_radio_transmit_power_custom', {'locator': {'default': self.page.locator('#wlan1_txpower')},
                                                 'type': 'fill'}),
            ('5g_radio_channel_width_20',
             {'locator': {'default': self.page.locator('div:has-text("5GHz Radio ")').locator('..').locator(
                 '//div[@class="ant-slider-mark"]/span[1]')}, 'type': 'button'}),
            ('5g_radio_channel_width_40',
             {'locator': {'default': self.page.locator('div:has-text("5GHz Radio ")').locator('..').locator(
                 '//div[@class="ant-slider-mark"]/span[2]')}, 'type': 'button'}),
            ('5g_radio_channel_width_80',
             {'locator': {'default': self.page.locator('div:has-text("5GHz Radio ")').locator('..').locator(
                 '//div[@class="ant-slider-mark"]/span[3]')}, 'type': 'button'}),
            ('5g_radio_channel_width_160',
             {'locator': {'default': self.page.locator('div:has-text("5GHz Radio ")').locator('..').locator(
                 '//div[@class="ant-slider-mark"]/span[4]')}, 'type': 'button'}),
            ('5g_radio_transmit_power',
             {'locator': {'default': self.page.locator('#wlan2_txpower_level')}, 'type': 'select',
              'param': {'auto': self.locale.auto, 'low': self.locale.radio_low, 'medium': self.locale.medium,
                        'height': self.locale.radio_height, 'custom': self.locale.custom}}),
            ('wireless_mesh', {'locator': {'default': self.page.locator('#mesh_enabled')}, 'type': 'switch_button'}),
            ('5g_transmit_power_custom', {'locator': {'default': self.page.locator('#wlan2_txpower')}, 'type': 'fill'}),
            ('save', {'locator': {'default': self.page.locator('//button[@class="ant-btn ant-btn-primary"]')},
                      'type': 'button'}),
            ('text_messages', {'type': 'text_messages'}),
            ('tip_messages', {'type': 'tip_messages'}),
            ('reset', {'locator': {'default': self.page.locator('//button[@class="ant-btn ant-btn-default"]')},
                       'type': 'button', "always_do": True}),
        ]

    @property
    @AdaptModelLocator.adapt_model
    def link_quality_history(self) -> list:
        return [
            ('interface_tab',
             {'locator': {'default': self.page.locator('//input[@type="search"]')}, 'type': 'select'}),
        ]

    @property
    @AdaptModelLocator.adapt_model
    def events(self) -> list:
        return [
            ('page_limit',
             {'locator': {'default': self.page.locator('//input[@type="search"]').last},
              'type': 'select', 'param': {10: f'10 {self.locale.page_limit}', 20: f'20 {self.locale.page_limit}',
                                          50: f'50 {self.locale.page_limit}', 100: f'100 {self.locale.page_limit}'}}),
            ('start_time',
             {'locator': {'default': self.page.locator('#timeRange')}, 'type': 'fill_date'}),
            ('end_time',
             {'locator': {'default': self.page.locator('//input[@placeholder="End date"]')}, 'type': 'fill_date'}),
            ('event_type',
             {'locator': {'default': self.page.locator('.ant-select-selection-overflow')}, 'type': 'select_more',
              'param': {'login_ok': self.locale.login_ok,
                        'login_fail': self.locale.login_fail,
                        'config': self.locale.config_c,
                        'cpu_high': self.locale.cpu_high,
                        'memory_high': self.locale.memory_high,
                        'vpn_state': self.locale.vpn_c,
                        'uplink_state': self.locale.uplink_c,
                        'uplink_switch': self.locale.uplink_s,
                        'wan2_lan1_s': self.locale.wan_s,
                        'uplink_detect': self.locale.detection_s,
                        'cellular_flow': self.locale.cellular_r,
                        'upgrade': self.locale.upgrade,
                        'reboot': self.locale.reboot, }}),
            ('clear_events',
             {'locator': {'default': self.page.locator(f'button:has-text("{self.locale.clear_events}")')},
              'type': 'button'}),
            ('export_events',
             {'locator': {'default': self.page.locator(f'button:has-text("{self.locale.export_events}")')},
              'type': 'download_file'}),
            ('cancel',
             {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-default"]'), 'type': 'button',
              "always_do": True}),
            ('action_confirm', {'locator': {'default': self.page.locator('.ant-popover-inner-content').locator(
                '.ant-btn.ant-btn-primary.ant-btn-sm').first},
                                'type': 'button'})
        ]

    @property
    @AdaptModelLocator.adapt_model
    def logs(self) -> list:
        return [
            ('line_limit',
             {'locator': {'default': self.page.locator('//input[@type="search"]').nth(1)},
              'type': 'select', 'param': {50: f'10 {self.locale.line}', 100: f'100 {self.locale.line}',
                                          200: f'50 {self.locale.line}', 500: f'500 {self.locale.line}'}}),
            ('level',
             {'locator': {'default': self.page.locator('#level')},
              'type': 'select', 'param': {'all': self.locale.all_logs, 'error': self.locale.error,
                                          'emergency': self.locale.emergency, 'serious': self.locale.serious,
                                          'warning': self.locale.warning, 'alarm': self.locale.alarm,
                                          'notice': self.locale.notice, 'information': self.locale.information,
                                          'debug': self.locale.debug}}),
            ('key',
             {'locator': {'default': self.page.locator('#keys')}, 'type': 'fill'}),
            ('search',
             {'locator': {'default': self.page.locator(f'button:has-text("{self.locale.search}")')},
              'type': 'button'}),
            ('reset',
             {'locator': {'default': self.page.locator(f'button:has-text("{self.locale.reset}")')},
              'type': 'button'}),
            ('refresh',
             {'locator': {'default': self.page.locator('//input[@type="search"]').nth(2)},
              'type': 'select',
              'param': {'manual_refresh': self.locale.manual_refresh, 5: f'5 {self.locale.seconds}',
                        10: f'10 {self.locale.seconds}', 15: f'15 {self.locale.seconds}',
                        60: f'1 {self.locale.minutes}'}}),
            ('reload',
             {'locator': {'default': self.page.locator('.anticon.anticon-reload')}, 'type': 'button'}),
            ('clear_logs',
             {'locator': {'default': self.page.locator(f'button:has-text("{self.locale.clear_logs}")')},
              'type': 'button'}),
            ('download_logs',
             {'locator': {'default': self.page.locator(f'button:has-text("{self.locale.download_logs}")')},
              'type': 'download_file'}),
            ('diagnostic_logs',
             {'locator': {'default': self.page.locator(f'button:has-text("{self.locale.diagnostic_logs}")')},
              'type': 'download_file'}),
            ('cancel',
             {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-default"]'), 'type': 'button',
              "always_do": True}),
            ('action_confirm', {'locator': {'default': self.page.locator('.ant-popover-inner-content').locator(
                '.ant-btn.ant-btn-primary.ant-btn-sm').first},
                                'type': 'button'})
        ]

    @property
    @AdaptModelLocator.adapt_model
    def device_information(self) -> list:
        return [
            ('name', {"locator": self.page.locator(
                'div:right-of(:text-is("{}"))'.format(self.locale.device_info_name)).nth(0), "type": 'text'}),
            ('model', {'locator': self.page.locator('.ant-descriptions-item-container', has=self.page.locator(
                f'span:has-text("{self.locale.device_info_model}")')).locator('//span[2]'), 'type': 'text'}),
            ('serial', {'locator': self.page.locator('.ant-descriptions-item-container', has=self.page.locator(
                f'span:has-text("{self.locale.device_info_serial}")')).locator('//span[2]'), 'type': 'text'}),
            ('firmware_version', {'locator': self.page.locator(
                '.ant-descriptions-item-container', has=self.page.locator(
                    f'span:has-text("{self.locale.device_info_firmware}")')).locator('//span[2]'), 'type': 'text'}),
            ('mac', {'locator': self.page.locator('.ant-descriptions-item-container', has=self.page.locator(
                f'span:has-text("{self.locale.device_info_mac}")')).locator('//span[2]'), 'type': 'text'}),
            ('uptime', {'locator': self.page.locator('.ant-descriptions-item-container', has=self.page.locator(
                f'span:has-text("{self.locale.device_info_uptime}")')).locator('//span[2]'), 'type': 'text'}),
            ('internet_access', {'locator': self.page.locator(
                '.ant-descriptions-item-container', has=self.page.locator(
                    f'span:has-text("{self.locale.device_info_internet_access}")')).locator('//span[2]'),
                                 'type': 'text'}),
            ('uplink_ip', {'locator': self.page.locator('.ant-descriptions-item-container', has=self.page.locator(
                f'span:has-text("{self.locale.device_info_uplink_ip}")')).locator('//span[2]'), 'type': 'text'}),
            ('local_gateway_ip', {'locator': self.page.locator(
                '.ant-descriptions-item-container', has=self.page.locator(
                    f'span:has-text("{self.locale.device_info_gateway}")')).locator('//span[2]'), 'type': 'text'}),
            ('system_time', {'locator': self.page.locator(
                '.ant-descriptions-item-container', has=self.page.locator(
                    f'span:has-text("{self.locale.device_info_systime}")')).locator('//span[2]'), 'type': 'text'}),
            ('license_status', {'locator': self.page.locator(
                '.ant-descriptions-item-container', has=self.page.locator(
                    f'span:has-text("{self.locale.device_info_license_status}")')).locator('//span[2]'),
                                'type': 'text'}),
        ]
