# -*- coding: utf-8 -*-
# @Time    : 2023/11/30 13:10:25
# @Author  : Pane Li
# @File    : adapt_model.py
"""
adapt_model, 用于适配不同型号的设备，对于不同型号的设备，其配置项locator 元素可能不同，需要对配置项做适配
所以所有的元素定位都使用locator 关键字, 最终会转换成对应的元素定位
{"locator": self.page.locator('#ipType')}
{"locator": {'default': self.page.locator('#ipType'), 'ER805': self.page.locator('#ipType')}},  'default' 必填
 在拿不到对应型号的locator时，会使用default 的locator
"""


class AdaptModelLocator:

    def __init__(self, model):
        self.model = model

    def rewrite_locator(self, data):
        """ 对于定义的locator做转换，需找出对应型号及版本的locator, 重写的必须带locator字段

        :param data:
        """
        if isinstance(data, dict):
            for key, value in data.items():
                if key == 'locator':
                    if isinstance(value, dict):
                        try:
                            data[key] = value.get(
                                list(filter(lambda x: self.model.upper() == x.upper(), value.keys()))[0])
                        except IndexError:
                            if value.get('DEFAULT'):
                                data[key] = value.get('DEFAULT')
                            elif value.get('default'):
                                data[key] = value.get('default')
                else:
                    self.rewrite_locator(value)
        elif isinstance(data, (tuple, list, set)):
            for item in data:
                self.rewrite_locator(item)

    def adapt_model(function):
        def __adapt_model(self, *args, **kwargs):
            res = function(self, *args, **kwargs)
            self.rewrite_locator(res)
            return res

        return __adapt_model


from playwright.sync_api import Page, sync_playwright


class ConfigLocators(AdaptModelLocator):
    def __init__(self, page: Page, locale: dict, model: str):
        super().__init__(model)
        self.page = page
        self.locale = locale
        self.pop_up = self.page.locator('.ant-modal-content')

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
                ('local_subnet_remove', {'locator': {
                    'default': self.page.locator('#local_subnet_0').locator('..').locator(
                        '.anticon.anticon-minus-circle')},
                    'type': 'click'}),
                ('local_subnet_add', {'locator': {
                    'default': self.page.locator('.ant-btn.ant-btn-dashed').first},
                    'type': 'button'}),
                ('local_subnet_0', {'locator': {'default': self.page.locator('#local_subnet_0')},
                                    'type': 'fill'}),
                ('local_subnet_1', {'locator': {'default': self.page.locator('#local_subnet_1')},
                                    'type': 'fill'}),
                ('local_subnet_2', {'locator': {'default': self.page.locator('#local_subnet_2')},
                                    'type': 'fill'}),
                ('local_subnet_3', {'locator': {'default': self.page.locator('#local_subnet_3')},
                                    'type': 'fill'}),
                ('remote_subnet_remove', {'locator': {
                    'default': self.page.locator('#remote_subnet_0').locator('..').locator(
                        '.anticon.anticon-minus-circle')},
                    'type': 'click'}),
                ('remote_subnet_add', {'locator': {
                    'default': self.page.locator('.ant-btn.ant-btn-dashed').last},
                    'type': 'button'}),
                ('remote_subnet_0', {'locator': {'default': self.page.locator('#remote_subnet_0')},
                                     'type': 'fill'}),
                ('remote_subnet_1', {'locator': {'default': self.page.locator('#remote_subnet_1')},
                                     'type': 'fill'}),
                ('remote_subnet_2', {'locator': {'default': self.page.locator('#remote_subnet_2')},
                                     'type': 'fill'}),
                ('remote_subnet_3', {'locator': {'default': self.page.locator('#remote_subnet_3')},
                                     'type': 'fill'}),
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
                'ike_policy_peer_status_detect', {'locator': {'default': self.page.locator('#ike_profile_dpd_enabled')},
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
        # return {"mode": self.page.locator('#ipType'), "mddd": self.page.locator('#ipType')}


if __name__ == '__main__':
    playwright = sync_playwright().start()
    browser = playwright.chromium
    browser = browser.launch(headless=False)
    context = browser.new_context(ignore_https_errors=True, permissions=['clipboard-read'])
    page = context.new_page()
    print(ConfigLocators(page, {}, 'EAP600').ipsec_vpn)
