# -*- coding: utf-8 -*-
# @Time    : 2023/7/5 13:33:07
# @Author  : Pane Li
# @File    : console.py
"""
console

"""
import logging
import allure
from inhandtest.tools import dict_in
from inhandtest.exception import ResourceNotFoundError
from inhandtest.inrequest.inrequest import InRequest


class Console:
    __doc__ = """nezha PaaS 后台 管理"""

    def __init__(self, password, host='star.nezha.inhand.design', proxy=False):
        """

        :param password  平台密码
        :param host: 'star.nezha.inhand.dev'|'star.nezha.inhand.design' 平台是哪个环境,
        """
        self.host = host
        self.api = InRequest(self.host, 'admin', password, 'star', proxy=proxy)

    def __get_org_info(self, org_email) -> dict:
        """ 获取org info

        :param org_email:
        :return:   {name: "Admin_test_new", email: "liwei@inhand.com.cn", _id: "5fb24ef9f0393a4c4fd7c8b7"}
        """
        orgs = self.api.send_request('/api/v1/orgs', 'get',
                                     param={'email': org_email, 'fields': '_id,name,email', 'limit': 100}).json().get(
            'result')
        if orgs:
            for org in orgs:
                if org.get('email') == org_email:
                    return org
            else:
                logging.exception(f'the org {org_email} not exist')
                raise ResourceNotFoundError(f'the org {org_email} not exist')
        else:
            logging.exception(f'the org {org_email} not exist')
            raise ResourceNotFoundError(f'the org {org_email} not exist')

    def __get_user_info(self, email) -> dict:
        users = self.api.send_request('/api/v1/users', 'get',
                                      param={'email': email, 'page': 0, 'limit': 100}).json().get('result')
        if users:
            for user in users:
                if user.get('email') == email:
                    return user
            else:
                logging.exception(f'the user {email} not exist')
                raise ResourceNotFoundError(f'the user {email} not exist')
        else:
            logging.exception(f'the user {email} not exist')
            raise ResourceNotFoundError(f'the user {email} not exist')

    def __get_product_info(self, product: str) -> dict:
        """ 获取产品信息

        :param product:
        :return:
        """
        products = self.api.send_request('/api/v1/products', 'get',
                                         param={'name': product, 'page': 0, 'limit': 100}).json().get('result')
        if products:
            for product_ in products:
                if product_.get('name') == product:
                    return product_
            else:
                logging.exception(f'the product {product} not exist')
                raise ResourceNotFoundError(f'the product {product} not exist')
        else:
            logging.exception(f'the product {product} not exist')
            raise ResourceNotFoundError(f'the product {product} not exist')

    @allure.step('PaaS为机构创建license')
    def create_license_to_org(self, org_email: str, licenses: dict):
        """ 创建license

        :param org_email: 企业邮箱
        :param licenses: license {'slug': 'star_pro', 'period': 'year', 'periodCount':1, 'number': 1}
        """
        license_prices = self.api.send_request(f'/api/v1/billing/license-types/{licenses.get("slug")}/prices', 'get',
                                               param={'verbose': 100}).json().get('result')
        org_info = self.__get_org_info(org_email)
        try:
            license_price = [i for i in license_prices if
                             i['period'] == licenses.get('period') and i['periodCount'] == licenses.get('periodCount')][
                0]
            self.api.send_request('/api/v1/billing/licenses', 'post',
                                  body={'type': licenses.get('slug'), 'active': True, 'count': licenses.get('number'),
                                        'oid': org_info.get('_id'), 'priceId': license_price['_id']}, code=200)
        except Exception:
            logging.exception(f'licenses create fail, please check the licenses info')
            raise

    @allure.step('PaaS获取许可证类型信息')
    def license_type_info(self, license_slug: str) -> dict:
        return self.api.send_request(f'/api/v1/billing/license-types/{license_slug}', 'get').json().get('result')

    @allure.step('PaaS许可证试用规则操作')
    def license_trials(self, action: str, **kwargs):
        """ PaaS管理许可证试用规则
        :param action: delete|add
        :param kwargs:
                product: 产品
                license_slug: 许可证类型
                days: 试用天数
                org_email: 机构邮箱  # 仅支持指定测试机构
        """
        oid = self.__get_org_info(kwargs.get('org_email')).get('_id')
        if action == 'add':
            payload = {'product': kwargs.get('product'), 'licenseId': kwargs.get('license_slug'),
                       'days': kwargs.get('days'), 'tid': oid}
            self.api.send_request(f'/api/v1/license-trials', 'post', body=payload, code=200)
            logging.info(f'license_trials add success')
        elif action == 'delete':
            _id = self.api.send_request(f'/api/v1/license-trials', 'get',
                                        param={'tid': oid, 'product': kwargs.get('product')}).json().get('result')[
                0].get('_id')
            self.api.send_request(f'/api/v1/license-trials/{_id}', 'delete', code=200)
            logging.info(f'license_trials delete success')

    @allure.step('PaaS管理许可试用记录')
    def device_trials(self, action: str, sn: str):
        """ PaaS管理许可试用记录
        :param action: delete|get
        :param  sn: 设备序列号
        """
        if len(sn) == 15:
            if action == 'delete':
                self.api.send_request(f'/api/v1/billing/device-trials/{sn}', 'delete')
                logging.info(f'device_trials delete success, sn: {sn}')
            elif action == 'get':
                tmp = self.api.send_request(f'/api/v1/billing/device-trials', 'get',
                                            param={'serialNumber': sn}).json().get('result')
                if tmp:
                    logging.info(f'sn: {sn} has trial records')
                    return True
                else:
                    logging.info(f'sn: {sn} has no trial record')
                    return False
        else:
            logging.info(f'sn: {sn}, length is not 15')

    @allure.step('PaaS管理机构收费策略')
    def org_accessible(self, accessible: bool, services: list, org_email: str):
        """ PaaS管理机构收费策略
        :param accessible: True|False
        :param services: 增值服务列表，['sd_wan', 'connector', 'project']
        :param org_email: 机构邮箱
        """
        oid = self.__get_org_info(org_email).get('_id')
        self.api.send_request(f'/api/v1/orgs/{oid}/accessible', 'put', body={'accessible': accessible,
                                                                             'premiumServices': services})
        logging.info(f'org: {org_email} update success, accessible: {accessible}, premiumServices: {services}')

    @allure.step('PaaS更新设备服务状态')
    def reset_service_status(self, product: str):
        """ PaaS更新某个产品型号下所有设备服务状态
        :param product: 产品型号
        """
        self.api.send_request(f'/api/v1/devices/reset-service-status', 'put', body={"product": product})
        logging.info(f'reset service status success, product: {product}')

    @allure.step('PaaS设备操作')
    def device(self, sn: str, action='delete', **kwargs):
        """

        :param sn: 设备序列号
        :param action: delete|info|add
        :param kwargs:
                org_email: 当删除时， 如果填写了org_email, 则删除该机构下的设备，如果sn 为None, 则删除该机构下所有设备
                state: {} 当获取到info 时 可以对 state 做判断
                name: 设备名称  当添加设备时，需要填写
                product: 设备产品  当添加设备时，需要填写
        :return:
        """
        if action == 'delete':
            oid = self.__get_org_info(kwargs.get('org_email')).get('_id') if kwargs.get('org_email') else None
            if sn:
                param = {'oid': oid, 'serial_number': sn, 'limit': 100, 'page': 0}
                _id = self.api.send_request(f'/api/v1/devices', 'get', param=param).json().get('result')[0].get('_id')
                self.api.send_request(f'api/v1/devices/{_id}', 'delete')
                logging.info(f'device {sn} delete success')
            else:
                if oid:
                    param = {'oid': oid, 'limit': 100, 'page': 0}
                    while True:
                        result = self.api.send_request(f'/api/v1/devices', 'get', param=param).json()
                        if result.get('total') == 0:
                            break
                        else:
                            for device in result.get('result'):
                                self.api.send_request(f'api/v1/devices/{device.get("_id")}', 'delete')
                                logging.debug(f'device {device.get("serialNumber")} delete success')
                    logging.info(f'admin delete {kwargs.get("org_email")} org all devices success')
        elif action == 'info':
            param = {'serial_number': sn, 'limit': 100, 'page': 0}
            result = self.api.send_request(f'/api/v1/devices', 'get', param=param).json().get('result')[0]
            dict_in(result, kwargs.get('state'))
        elif action == 'add':
            body = {"name": kwargs.get('name'), "serialNumber": sn, "product": kwargs.get('product')}
            self.api.send_request('/api/v1/devices', 'post', body=body)

    @allure.step('PaaS用户操作')
    def user(self, email: str, action='update_password', **kwargs):
        """

        :param email: 用户邮箱
        :param action: update_password|delete
                    update_password:
                        password

        :param kwargs:
               password: 新密码
        :return:
        """
        user = self.__get_user_info(email)
        user_id, oid = user.get('_id'), user.get('oid')
        if action == 'update_password':
            self.api.send_request(f'/api/v1/users/{user_id}/password', 'put', body={'password': kwargs.get('password')})
            logging.info(f'the {email} user password update success')
        elif action == 'delete':
            try:
                self.api.send_request(f'api/v1/users/{user_id}', 'delete', param={'oid': oid})
                logging.info(f'the {email} user delete success')
            except Exception:
                logging.exception(f'the email be used by org, can not delete')

    @allure.step('PaaS机构操作')
    def org(self, org_email: str, action='create', **kwargs) -> dict or None:
        """

        :param org_email:
        :param action: create|delete|find
        :param kwargs:
                password:  create
                force: True|False  create 当为True时，如果org已存在，删除org，创建新的org
                                          当为False时，如果org已存在，就不删除，只是更新该org_mail 用户的密码， 使其同步
        :return:
        """
        if action == 'create':
            org_info = {'email': org_email, 'password': kwargs.get('password'), 'name': org_email,
                        'bizCategory': 'OILS_GAS_CONSUMABLE_FUELS', 'countryCode': 'AL'}
            try:
                self.__get_org_info(org_email)
                if kwargs.get('force'):  # 删除org，创建新的org
                    self.org(org_email, action='delete')
                    self.api.send_request('api/v1/orgs', 'post', body=org_info)
                    logging.debug(f'admin create {org_info.get("email")} org success')
                else:
                    self.user(org_email, action='update_password', password=kwargs.get('password'))
                    logging.debug(f'admin update {org_info.get("email")} org success')
            except ResourceNotFoundError:
                try:
                    self.user(org_email, 'delete')  # 删除该用户邮箱
                except ResourceNotFoundError:
                    pass
                self.api.send_request('api/v1/orgs', 'post', body=org_info)
                logging.debug(f'admin create {org_info.get("email")} org success')
        elif action == 'delete':
            org_id = self.__get_org_info(org_email).get('_id')
            self.device(sn='', action='delete', org_email=org_email)
            self.api.send_request(f'api/v1/orgs/{org_id}', 'delete')
            logging.info(f'admin delete {org_email} org success')
        elif action == 'find':
            return self.__get_org_info(org_email)

    @allure.step('获取产品相关信息')
    def get_product(self, product='ER805', type_='support_function') -> dict:
        """

        :param product:
        :param type_: support_function
                    :return {function_id: minVersion}
        :return:
        """
        _id = self.__get_product_info(product).get('_id')
        if type_ == 'support_function':
            functions = self.api.send_request(f'/api/v1/products/{_id}/compatibilities', 'get',
                                              {"limit": 100, "page": 0}).json().get('result')
            return {function.get('compatibilityId'): function.get('minVersion') for function in functions if
                    function.get('support')}
        elif type_ == 'info':
            return self.api.send_request(f'/api/v1/products/{_id}', 'get').json().get('result')


if __name__ == '__main__':
    from inhandtest.log import enable_log

    enable_log(console_level='debug')
    console = Console('admin', 'star.nezha.inhand.design')
    console.org_accessible(False, [], 'wangzhim@inhand.com.cn')
