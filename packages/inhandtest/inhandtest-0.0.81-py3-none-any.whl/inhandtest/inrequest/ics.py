# -*- coding: utf-8 -*-
# @Time    : 2023/7/5 13:19:42
# @Author  : Pane Li
# @File    : ics.py
"""
ics

"""
import logging
import re
import time
from typing import List
from inhandtest.tools import loop_inspector
from inhandtest.inrequest import DmInterface
from inhandtest.exception import ResourceNotFoundError


class IcsInterface(DmInterface):
    __slots__ = ['remote_maintenance_online']

    def __init__(self, username, password, host='ics.inhandiot.com', proxy=False, headers=None):
        """
        :param username  平台用户名
        :param password  平台密码
        :param host: 'ics.inhandiot.com'|'ics.inhandnetworks.com' 平台是哪个环境
        """
        super().__init__(username, password, host, proxy=proxy, headers=headers)
        self.oid = self.__oid()

    def __oid(self) -> str:
        return self.api.send_request('api/me', 'get', {'verbose': 100}).json().get('result').get('oid')

    def add_device(self, sn_model: dict):
        """添加设备，

        :param sn_model: {$sn: 'IR302', $sn1: 'IR305'}
                model: IR901|IR912|IG902|IR915-WiFi|IG902-WiFi|VG710|IR915|IR611|IR615|IR301|IR302|IR305|IG501|IG502|IG532|IG974|VG814,
                    型号内容必须填写正确，不然添加的时候下发OpenVpn的配置会出问题，导致不能正常连接
        :return:
        """
        if sn_model:
            models = self.api.send_request('api/invpn/routers/models', 'get').json().get('result').get('models')
            for sn, model in sn_model.items():
                for model_ in models:
                    if model == model_.get('name'):
                        lan_interface = model_.get('lanInterface')
                        if len(re.findall(model_.get('serialNumberPattern'), sn)) == 1:
                            subnet = self.api.send_request('api/invpn/router/subnet', 'get').json().get('result')
                            body = {'serialNumber': sn, 'name': sn + str(int(time.time())),
                                    'lanInterface': lan_interface,
                                    'subnet': subnet}
                            self.api.send_request('api/invpn/router', 'post', {'oid': self.oid}, body=body)
                            logging.info(f'add device {sn} to cloud {self.host} successfully')
                        break
                else:
                    logging.exception(f'the Serial number {sn} and model do not match ')
                    raise Exception(f'the Serial number {sn} and model do not match ')

    def find_device(self, param=None, **kwargs) -> list[dict]:
        """

        :param kwargs:  online: 1|0
        :param param:  {'serialNumber': sn}
        :return:
        """
        result = []
        for i in range(0, 100):
            response = self.api.send_request('api/invpn/routers', method='get',
                                             param={**{"limit": 100, "cursor": i * 100, 'verbose': 100}, **param}).json()
            if response.get('result'):
                for res in response.get('result'):
                    for key, value in kwargs.items():
                        if res.get(key) != value:
                            break
                    else:
                        result.append(res)
            if len(response.get('result')) < 100:
                break
        return result

    def find_user(self, **kwargs) -> list:
        """

        :param kwargs:  online: 1|0
        :return:
        """
        result = []
        for i in range(0, 100):
            response = self.api.send_request('api/invpn/users', method='get',
                                             param={"limit": 100, "cursor": i * 100, 'verbose': 100}).json()
            if response.get('result'):
                for res in response.get('result'):
                    for key, value in kwargs.items():
                        if res.get(key) != value:
                            break
                    else:
                        result.append(res)
            if len(response.get('result')) < 100:
                break
        if not result:
            raise ResourceNotFoundError(f'the user {kwargs} not exist')
        return result

    def device_state(self, sn: list) -> List[dict]:
        """根据sn 转换属性 属性值有：  online: 在线|离线   1|0
                                       connected: true | None
                                       iccid:
                                       imei:
                                       imsi:
                                       version: 固件版本
                                       hwVersion: 硬件版本 'V1.0'
                                       bootVersion:  Bootloader版本  '1.1.3.r4956'
                                       sn: 序列号
                                       id: 设备id
                                       name: 设备名称
                                       vip: 虚拟IP
                                       ip: 设备连接平台的ip地址
                                       protocol: 设备连接平台的协议
                                       config_sync: 设备配置同步状态
        :param sn: 列表
        :return: [{'sn': $sn, 'online': 1, 'iccid': '', 'imei'}]
        """
        result = []
        for sn_ in sn:
            response = self.api.send_request('api/invpn/routers', method='get',
                                             param={"limit": 10, "cursor": 0, 'verbose': 100,
                                                    'serialNumber': sn_}).json()
            if response.get('total') == 1:
                logging.debug(f'the device {sn_} exist on {self.host}')
                res = response.get('result')[0]
                res_info = self.api.send_request(f'api/devices/{res.get("id")}', method='get',
                                                 param={'verbose': 100}).json().get('result')
                config_sync = res_info.get('config').get('sync') if res_info.get('config') else None
                result.append(
                    {'sn': sn_, 'online': res.get('online'), 'iccid': res.get('metadata').get('iccid'),
                     'imei': res.get('metadata').get('imei'), 'imsi': res.get('metadata').get('imsi'),
                     'version': res.get('metadata').get('swVersion'), 'hwVersion': res.get('metadata').get('hwVersion'),
                     'bootVersion': res.get('metadata').get('bootVersion'), 'vip': res.get('vip'),
                     'id': res.get('id'), 'connected': res.get('connected'), 'name': res.get('name'),
                     'ip': res_info.get('pubIp'), 'protocol': res_info.get('protocol'), 'config_sync': config_sync})
            else:
                result.append(
                    {'sn': sn_, 'online': None, 'iccid': None, 'imei': None, 'imsi': None, 'version': None,
                     'hwVersion': None, 'bootVersion': None, 'id': None, 'connected': None, 'name': None, 'ip': None,
                     'protocol': None, 'config_sync': None, 'vip': None})
        return result

    def send_openvpn_config(self, sn: str) -> None:
        """每次把设备添加到平台上线后，openvpn要连半天，可以主动推送下配置让openvpn连接的更快，
           如果设备已经连接上了openvpn就不在下发了

        :param sn: 单个sn
        :return:
        """
        result = self.device_state([sn])[0]
        if result.get('online') and not result.get('connected'):
            self.api.send_request(f'api/invpn/router/{result.get("id")}/config/send', 'get', param={'oid': self.oid})
        elif not result.get('id'):
            logging.warning(f'the device {sn} not exist')
        elif not result.get('online'):
            logging.warning(f'the device {sn} offline')
        elif result.get('connected'):
            logging.warning(f'the device {sn} already connected')

    def delete_device(self, sn: str or list, param=None) -> None:
        """

        :param sn: 设备序列号，一个或多个
        :param param:  {'online': True}
        :return:
        """
        sn = [sn] if isinstance(sn, str) else sn
        for device in self.find_device(param=param):
            if (sn and device.get('serialNumber') in sn) or (not sn):
                self.api.send_request(f'api/invpn/router/{device.get("id")}', 'delete', {'oid': self.oid})
                logging.info(f'the {device.get("serialNumber")} delete success')

    @loop_inspector('ics user connect openvpn')
    def assert_user_openvpn_connect(self, email, timeout=60, interval=5):
        response = self.api.send_request('/api/invpn/users', 'get', param={'verbose': 100, 'email': email}).json()
        return response['result'][0]['connected']

    def download_openvpn_config(self, email: str, file_path: str) -> None:
        """

        :param email: 用户邮箱
        :param file_path: 配置文件路径， 如./smoke@inhand.com.cn.ovpn
        :return:
        """
        uid = self.find_user(email=email)[0].get('_id')
        self.api.send_request('/api/invpn/client.ovpn', 'get', file_path=file_path,
                              param={'uid': uid, 'oid': self.oid, 'comp-lzo': True})

    def add_endpoint(self, sn: str, number: int = 1) -> None:
        """添加终端，当前未调试

        :param sn : 设备序列号
        :param number: 添加的数量,
        :return:
        """
        if sn:
            route_id = self.find_device({"serialNumber": sn})[0].get('id')
            ip_start = 0
            for i in range(0, number):
                vip = self.api.send_request(f'api/invpn/router/{route_id}/endpoint/vip', 'get').json().get('result')
                if i and i % 255 == 0:
                    ip_start += 1
                ip = f'192.168.{ip_start}.{i % 255}'
                self.api.send_request(f'api/invpn/router/{route_id}/endpoint', 'post',  body={'ip': ip, 'name': ip, 'vip': vip})




