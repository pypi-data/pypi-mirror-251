# -*- coding: utf-8 -*-
# @Time    : 2023/11/3 14:03:18
# @Author  : Pane Li
# @File    : link.py
"""
link

"""
import allure
from inhandtest.tools import dict_merge

from inhandtest.inrequest.inrequest import InRequest
from inhandtest.inrequest.nezha import Base


class Plan(Base):

    def __init__(self, api, email, host):
        super().__init__(api, email, host)

    @allure.step('获取套餐规格')
    def find(self, param: dict = None) -> list:
        """

        :param param: 查询参数
        :return:
        """
        return self.api.send_request(f'/api/v1/link/plans', 'get',
                                     dict_merge({"limit": 100, "page": 0, 'expand': 'planType'}, param)).json().get(
            'result')

    @allure.step('获取优惠')
    def coupons(self, param: dict = None) -> dict:
        return self.api.send_request(f'/api/v1/link/orders/coupons', 'get', param).json().get('result')


class PlanType(Base):

    def __init__(self, api, email, host):
        super().__init__(api, email, host)

    @allure.step('获取套餐类型')
    def find(self, param: dict = None) -> list:
        """

        :param param: 查询参数
        :return:
        """
        return self.api.send_request(f'/api/v1/link/plan-types', 'get',
                                     dict_merge({"limit": 100, "page": 0}, param)).json().get('result')


class Order(Base):
    def __init__(self, api, email, host):
        super().__init__(api, email, host)
        self.__plan = Plan(api, email, host)

    @allure.step("下订单")
    def add_order(self, plan: str, address: dict, sim_count=1) -> dict:
        """
        :param plan: 套餐名称
        :param address: 地址信息
        :param sim_count: sim卡数量
        :return:
        """
        plan_ = self.__plan.find({"name": plan})[0]
        product = plan_.get('planType').get('products')[0].get('name')
        sim_one_time_fee = self.__plan.coupons({'planId': plan_.get('_id'), "productName": product}).get('oneTimeFees')[
            0]
        body = {"carrier": plan_.get('planType').get('carrier'), "simCount": sim_count,
                "addresses": address, "product": product, "planType": plan_.get('planType').get('name'),
                "plan": plan, "includedUsage": plan_.get('includedUsage'), "simOneTimeFee": sim_one_time_fee}
        return self.api.send_request(f'/api/v1/link/orders', 'post', body=body).json().get('result')


class Businesses(Base):

    def __init__(self, api, email, host):
        super().__init__(api, email, host)

    def add(self, iccids: list, body: dict, type_="add_targeted_addresses", notes: str = '') -> dict:
        """添加业务工单

        :param iccids: iccids 列表
        :param body: 业务工单请求体 {"addresses": ["122222221333"]}
        :param type_: 业务工单类型 add_targeted_addresses|delete_targeted_addresses
        :param notes: 备注
        :return:
        """
        body = {"type": type_, "iccidInputType": 'list', "iccids": iccids, "notes": notes, **body}
        return self.api.send_request(f'/api/v1/link/businesses/targeted-groups', 'post', body=body).json()

    def find(self, param: dict = None) -> list:
        result = []
        for i in range(0, 100):
            response = self.api.send_request('/api/v1/link/businesses', method='get',
                                             param={**param, **{'expand': 'org', 'limit': 100, 'page': i}}).json()
            if response.get('result'):
                for res in response.get('result'):
                    result.append(res)
            if len(response.get('result')) < 100:
                break
        return result


class LinkInterface:

    def __init__(self, email, password, host='star.inhandcloud.cn', proxy=False, **kwargs):
        """ 须确保用户关闭了多因素认证

        :param email  平台用户名
        :param password  平台密码
        :param host: 'star.inhandcloud.cn'|'star.inhandcloud.cn'|'star.nezha.inhand.dev'|'star.nezha.inhand.design' 平台是哪个环境,
        :param proxy: 是否使用代理
        :param kwargs:
            body_remove_none_key: 是否删除请求体中的空值
            param_remove_none_key: 是否删除请求参数中的空值
        """

        self.api = InRequest(host, email, password, 'star',
                             body_remove_none_key=kwargs.get('body_remove_none_key', True),
                             param_remove_none_key=kwargs.get('param_remove_none_key', True),
                             proxy=proxy)
        self.plan = Plan(self.api, email, host)
        self.order = Order(self.api, email, host)
        self.businesses = Businesses(self.api, email, host)


if __name__ == '__main__':
    from inhandtest.log import enable_log

    enable_log(console_level='debug')
    link = LinkInterface('liwei@inhand.com.cn', '123456', 'star.nezha.inhand.design')
    for i in range(0, 1):
        link.businesses.add(['898604932922C0028085'], {
            "addresses": ["*.iot.inhand.com.cn"]})
