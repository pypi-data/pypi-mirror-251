# -*- coding: utf-8 -*-
# @Time    : 2023/11/23 14:13:31
# @Author  : Pane Li
# @File    : oms.py
"""
oms

"""
from inhandtest.exception import ResourceNotFoundError
from inhandtest.file import file_content_read
from inhandtest.inrequest import Console
from inhandtest.inrequest.link import Plan, PlanType


class UsagePool:
    def __init__(self, api, host, console: Console):
        self.api = api
        self.plan = Plan(api, 'admin', host)
        self.console = console

    def info(self, name: str, type_='list') -> dict:
        """获取流量池信息
        :param name: 名称
        :param type_:  list|detail,  分别返回的是列表或者详情
        :return:
        """
        try:
            info = self.find({'name': name})[0]
        except Exception:
            raise ResourceNotFoundError(f'the usage pool {name} not exist')
        if type_ == 'list':
            return info
        else:
            return self.api.send_request(f'/api/v1/link/usage-pools/{info["_id"]}', method='get',
                                         param={'expand': 'plan,org,cycleUsage,cardCount'}).json().get('result')

    def add(self, name: str, org_email: str, data_plan, notes: str = '') -> dict:
        """添加流量池

        :param name: 流量池名称
        :param org_email: str
        :param data_plan:
        :param notes: 备注
        :return:
        """
        try:
            plan_id = self.plan.find({"name": data_plan, "status": 'published'})[0].get('_id')
        except IndexError:
            raise IndexError(f'plan {data_plan} not found or unpublished')
        oid = self.console.org(org_email, 'find').get('_id')
        body = {"name": name, "oid": oid, "planId": plan_id, "notes": notes}
        return self.api.send_request(f'/api/v1/link/usage-pools', 'post', body=body).json()

    def find(self, param: dict = None) -> list:
        result = []
        for i in range(0, 100):
            response = self.api.send_request('/api/v1/link/usage-pools', method='get',
                                             param={**param, **{'expand': 'plan,org,cycleUsage,cardCount',
                                                                'limit': 100, 'page': i}}).json()
            if response.get('result'):
                for res in response.get('result'):
                    result.append(res)
            if len(response.get('result')) < 100:
                break
        return result

    def delete(self, name: str) -> dict:
        """删除流量池

        """

        return self.api.send_request(f'/api/v1/link/usage-pools/{self.info(name).get("_id")}', 'delete').json()

    def add_cards(self, iccids: str or list, name):
        """添加卡到流量池

        :param iccids: str or list, 后台在处理时不超过1000个
        :param name: 流量池名称
        :return:
        """
        iccids = iccids if isinstance(iccids, list) else [iccids]
        return self.api.send_request(f'/api/v1/link/usage-pools/{self.info(name).get("_id")}/cards', 'post',
                                     body={"iccids": iccids}).json()

    def remove_cards(self, iccids: str or list, name):
        """批量移除卡

        :param iccids:
        :param name:
        :return:
        """
        iccids = iccids if isinstance(iccids, list) else [iccids]
        return self.api.send_request(f'/api/v1/link/usage-pools/{self.info(name).get("_id")}/cards/bulk-remove', 'post',
                                     body={"iccids": iccids}).json()

    def sync_usages(self, name: str) -> dict:
        """ 同步流量池中所有卡的使用量

        :param name:
        :return:
        """
        return self.api.send_request(f'/api/v1/link/usage-pools/{self.info(name).get("_id")}/sync-usages',
                                     'post').json()


class Packages:

    def __init__(self, api, host, console: Console):
        self.api = api
        self.plan_type = PlanType(api, 'admin', host)
        self.console = console

    def add(self, pkg_id: str, name: str, carrier: str, plan_type: str, quota: int, price: int, desc: str,
            published=True) -> dict:
        """添加加油包
            param: pkg_id: 加油包id
            param: name: 加油包名称
            param: carrier: 运营商 ChinaUnicom|ChinaMobile|ChinaTelecom|Verizon|ATT
            param: plan_type: 套餐类型
            param: quota: 加油包额度，单位：Byte
            param: price: 加油包价格，单位：分
            param: desc: 描述
            param: published: 是否发布
        """
        try:
            plan_type_name = self.plan_type.find({"carrier": carrier, "name": plan_type})[0].get('name')
        except Exception:
            raise ResourceNotFoundError(f'{plan_type} not found')
        body = {"id": pkg_id, "name": name, "carrier": carrier, "planTypeName": plan_type_name, "quota": quota,
                "price": price, "published": published, "description": desc}
        return self.api.send_request(f'/api/v1/link/packages', 'post', body=body).json()

    def update(self, pkg_id: str, price: int, desc: str, published=True) -> dict:
        """更新加油包
            param: pkg_id: 加油包id
            param: price: 加油包价格，单位：分
            param: desc: 描述
            param: published: 是否发布
        """
        body = {"price": price, "published": published, "description": desc}
        return self.api.send_request(f'/api/v1/link/packages/{pkg_id}', 'put', body=body)

    def delete(self, pkg_id: str) -> dict:
        """删除加油包
            param: pkg_id: 加油包id
        """
        return self.api.send_request(f'/api/v1/link/packages/{pkg_id}', 'delete')

    def find(self, name=None, carrier=None) -> list:
        """
        :param name: 查询参数，加油包名称
        :param carrier: 运营商名称 ChinaUnicom|ChinaMobile|ChinaTelecom|Verizon|ATT
        :return: list
        """
        result = []
        for i in range(0, 100):
            response = self.api.send_request('/api/v1/link/packages', method='get',
                                             param={'name': name, 'carrier': carrier, 'limit': 100, 'page': i}).json()
            if response.get('result'):
                for res in response.get('result'):
                    result.append(res)
            if len(response.get('result')) < 100:
                break
        return result


class TargetedGroups:

    def __init__(self, api, console: Console):
        self.api = api
        self.console = console

    def add(self, name: str, carrier: str, org_email: str, addresses: list, iccid_ls: list, notes: str) -> dict:
        """添加定向群组
            param: name: 加油包名称
            param: carrier: 运营商 ChinaUnicom|ChinaMobile|ChinaTelecom|Verizon|ATT
            param: org_email: 组织邮箱
            param: addresses: 地址列表
            param: iccid_ls: iccid列表
            param: notes: 备注
        """
        body = {"name": name, "carrier": carrier, "oid": self.console.org(org_email, 'find').get('_id'),
                "addresses": addresses, "iccids": iccid_ls, "notes": notes}
        return self.api.send_request(f'/api/v1/link/targeted-groups', 'post', body=body).json()

    def delete(self, group_id: str) -> dict:
        """删除定向群组
            param: group_id: 定向群组id
        """
        return self.api.send_request(f'/api/v1/link/targeted-groups/{group_id}', 'delete')

    def update(self, group_id: str, name: str, addresses=None) -> dict:
        """更新定向群组
            param: group_id: 定向群组id
            param: name: 定向群组名称
            param: addresses: list, 定向地址列表
        """
        body = {"name": name, "addresses": addresses}
        return self.api.send_request(f'/api/v1/link/targeted-groups/{group_id}', 'put', body=body).json()

    def summary(self) -> dict:
        return self.api.send_request('/api/v1/link/cards/targeted-summary', method='get').json().get('result')

    def info(self, name: str = None, org_email: str = None, type_='list') -> dict:
        """获取定向群组信息
        :param name: 名称
        :param org_email: 组织邮箱
        :param type_:  list|detail,  分别返回的是列表或者详情
        :return:
        """
        try:
            info = self.find(name, org_email)[0]
        except Exception:
            raise ResourceNotFoundError(f'targeted groups not exist')
        if type_ == 'list':
            return info
        else:
            return self.api.send_request(f'/api/v1/link/targeted-groups/{info["_id"]}', method='get',
                                         param={'expand': 'org,targetedGroupCards'}).json().get('result')

    def find(self, name: str = None, org_email: str = None) -> list:
        """
        :param name: 查询参数，定向群组名称
        :param org_email: 组织邮箱
        :return:
        """
        result = []
        for i in range(0, 100):
            response = self.api.send_request('/api/v1/link/targeted-groups', method='get', param={
                'name': name, 'oid': self.console.org(org_email, 'find').get('_id') if org_email else None,
                'limit': 100, 'page': i, 'expand': 'org,plan'}).json()
            if response.get('result'):
                for res in response.get('result'):
                    result.append(res)
            if len(response.get('result')) < 100:
                break
        return result

    def assign_cards(self, name: str, org_email: str, iccid_ls: list):
        """添加卡到定向群组
        param: name: 定向群组名称
        param: org_email: 组织邮箱
        param: iccid_ls: iccid列表
        return:
        """
        temp = self.find(name, org_email)[0].get('_id')
        return self.api.send_request(f'/api/v1/link/targeted-groups/{temp}/assign-cards', 'put',
                                     body={"iccids": iccid_ls}).json()


class Oms:
    def __init__(self, password, host='star.nezha.inhand.design', proxy=False):
        self.console = Console(password, host, proxy)
        self.usage_pool = UsagePool(self.console.api, host, self.console)
        self.packages = Packages(self.console.api, host, self.console)
        self.targeted_groups = TargetedGroups(self.console.api, self.console)


if __name__ == '__main__':
    from inhandtest.log import enable_log

    iccids = file_content_read('./sim20000.csv')
    enable_log(console_level='debug')
    oms = Oms('admin')
    for i in range(100, 1, -1):
        oms.usage_pool.delete(f"test_{i}")
    # oms.usage_pool.add_cards(['898604932922C0028084', '898604932922C0028085'], '宁夏110M')
    # oms.usage_pool.remove_cards(['898604932922C0028084', '898604932922C0028085'], '宁夏110M')
    # for i in range(0, 10):
    #     oms.usage_pool.remove_cards(iccids[i * 1000:(i + 1) * 1000], '月结5G')
    # for i in range(0, 10):
    #     oms.usage_pool.add_cards(iccids[i * 1000:(i + 1) * 1000], '月结5G')
    # for i in range(8, 1, -1):
    #     oms.usage_pool.delete(f'pool_{i}')
    # print(oms.packages.add('test', 'test', 'ChinaTelecom', 'IOT 3G', 1024, 100, 'test'))
