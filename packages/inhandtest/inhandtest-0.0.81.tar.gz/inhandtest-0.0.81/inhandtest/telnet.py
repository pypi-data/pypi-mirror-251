# -*- coding: utf-8 -*-
# @Time    : 2023/2/7 15:56:30
# @Author  : Pane Li
# @File    : telnet.py
"""
telnet

"""
import os
import re
import telnetlib
import time
from typing import List
import dynaconf
from inhandtest.tools import loop_inspector, replace_str
import logging


class Telnet:
    __doc__ = '使用telnet连接设备，封装下面命令'

    def __init__(self, model: str, host: str, super_user: str, super_password: str, user='adm', password='123456',
                 port=23, **kwargs):
        """使用telnet连接设备

        :param model: 设备型号，VG710'|'IR302'|'ER805'|'ER605'|'IG902'|'IG502'|'IR915'|'ODU2002'|'IR305'|'IR615'|IR624
        :param host: 设备lan ip， 192.168.2.1
        :param super_user: 超级管理员的用户名称
        :param super_password:  超级管理员的密码
        :param user: 用户名
        :param password: 用户密码
        :param port: 端口
        :param kwargs: interface_replace, 字典类型，只替换输入命令 {'wan': 'wan0', 'wifi_sta': 'wan2', 'cellular1': 'wwan0'}
                       在telnet里面接口名称转换，使得输入命令时接口名称统一。
                       factory_username:  工厂用户名
                       factory_password: 工厂用户密码
                       connect_timeout: 10  默认10秒
                       connect_interval: 10, 最大20， 一般不需要修改

        """
        self.model = model.upper()
        self.host = host
        self.super_user = super_user
        self.super_password = super_password
        self.user = user
        self.password = password
        self.port = port
        self.connect_timeout = kwargs.get('connect_timeout', 10)
        self.connect_interval = kwargs.get('connect_interval', 10)
        self.connect_interval = 20 if self.connect_interval > 20 else self.connect_interval  # 最大20秒
        self.connect_interval = self.connect_timeout if self.connect_interval > self.connect_timeout else self.connect_interval  # 不能超过connect_timeout
        self.host_name = ''
        self.super_tag = r'\/[a-zA-Z0-9_\/]* #'
        self.config_tag = '(config)#'
        self.user_tag = '#'  # 特权模式
        self.normal_tag = '>'
        self.factory_tag = '(factory)#'  # 仅部分设备支持工厂模式
        self.factory_username = kwargs.get('factory_username')
        self.factory_password = kwargs.get('factory_password')
        self.interface_replace: dict = kwargs.get('interface_replace')
        self.setting = dynaconf.Dynaconf(settings_files=[os.path.join(os.path.dirname(__file__), 'telnet.yaml')])
        self.tn: telnetlib.Telnet
        self.__login()

    def __get_mode_switch_cli(self, mode_config: dict) -> List[str]:
        """ 获取模式切换命令

        :param mode_config: 切换配置项内容
        :return:
        """
        for key, value in mode_config.items():
            if re.search(self.model, key, re.I):
                cli = value
                break
        else:
            cli = mode_config.default
        return cli

    def update_hostname(self, hostname: str) -> None:
        """更新hostname 后对应的telnet也需要更新

        :param hostname: str
        :return:
        """
        self.host_name = hostname
        self.user_tag = f'{hostname}#'
        self.normal_tag = f'{hostname}>'

    def __login(self):
        """


        :return:
        """
        for key, value in self.setting.login_spe.items():
            if re.search(self.model, key, re.I):
                login_spe = value
                break
        else:
            login_spe = self.setting.login_spe.default
        for i in range(0, self.connect_timeout, self.connect_interval):
            try:
                # 连接telnet服务器
                logging.debug("Start telnet 【%s:%s】" % (self.host, self.port))
                self.tn = telnetlib.Telnet(self.host, self.port, timeout=self.connect_interval)
                logging.debug("Telnet 【%s:%s】 connected" % (self.host, self.port))
                break
            except Exception:
                logging.warning(f'telnet connect {self.host}:{self.port} failed】, try again')
        else:
            logging.exception(f'ConnectionError Device【{self.host}:{self.port} connect failed】')
            raise ConnectionError(f'Device【{self.host}:{self.port} connect failed】')
        if self.model not in ['ER2000']:
            self.tn.write("\n".encode("cp936"))
        logging.debug(self.tn.read_until('login:'.encode("cp936")).decode("cp936").strip())
        # 登录路由器
        self.tn.write("{}\n".format(self.user).encode("cp936"))
        logging.debug(self.tn.read_until('Password:'.encode("cp936")).decode("cp936").strip())
        self.tn.write("{}\n".format(self.password).encode("cp936"))
        login_result = self.tn.read_until(login_spe.encode("cp936"), timeout=20).decode("cp936").strip()
        logging.debug(login_result)
        if 'Login incorrect' in login_result:
            logging.exception('UsernameOrPasswordError')
            raise Exception('UsernameOrPasswordError')
        self.update_hostname(login_result.split('\r\n')[-1].split(' ')[-1][:-1])
        logging.info(f"Device {self.host} login success. user_tag: {self.user_tag}")
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __auto_login(function):
        """自动重新登录, 只能当装饰器使用， 不对外使用

        :param function:
        :return:
        """

        def __auto_login(self, *args, **kwargs):
            try:
                res = function(self, *args, **kwargs)
            except (ConnectionResetError, ConnectionAbortedError):
                self.__login()
                res = function(self, *args, **kwargs)
            return res

        return __auto_login

    @__auto_login
    def super_mode(self) -> None:
        """进入路由器的超级模式

        @return:
        """
        self.tn.write(("\003" + "\r").encode("cp936"))
        time.sleep(1)
        read_contents = self.tn.read_very_eager().decode('cp936').strip()
        logging.debug(read_contents)
        switch_mode = None
        if self.config_tag in read_contents:
            switch_mode = 'config_mode'
        elif self.user_tag in read_contents:
            switch_mode = 'user_mode'
        elif self.normal_tag in read_contents:
            switch_mode = 'normal_mode'
        elif self.factory_tag in read_contents:
            switch_mode = 'factory_mode'
        elif re.search(self.super_tag, read_contents):
            pass
        else:
            logging.warning(f'not support this mode. telnet return contents: {read_contents}')
            self.close()
            self.__login()
            self.super_mode()
        if switch_mode:
            self.send_cli(self.__get_mode_switch_cli(self.setting.get(switch_mode).get('super_mode')),
                          key_replace={'super_user': self.super_user, 'super_password': self.super_password,
                                       'pwd': self.password, 'factory_user': self.factory_username,
                                       'factory_password': self.factory_password}, key_replace_type='cli')
        logging.info(f"Device {self.host} access in super mode")

    @__auto_login
    def config_mode(self) -> None:
        """配置模式

        :return:
        """
        self.tn.write(("\003" + "\r").encode("cp936"))
        time.sleep(1)
        read_contents = self.tn.read_very_eager().decode('cp936').strip()
        logging.debug(read_contents)
        switch_mode = None
        if self.config_tag in read_contents:
            pass
        elif self.user_tag in read_contents:
            switch_mode = 'user_mode'
        elif self.normal_tag in read_contents:
            switch_mode = 'normal_mode'
        elif self.factory_tag in read_contents:
            switch_mode = 'factory_mode'
        elif re.search(self.super_tag, read_contents):
            switch_mode = 'super_mode'
        else:
            logging.warning(f'not support this mode, last content:{read_contents}')
            self.close()
            self.__login()
            self.config_mode()
        if switch_mode:
            self.send_cli(self.__get_mode_switch_cli(self.setting.get(switch_mode).get('config_mode')),
                          key_replace={'super_user': self.super_user, 'super_password': self.super_password,
                                       'pwd': self.password, 'factory_user': self.factory_username,
                                       'factory_password': self.factory_password}, key_replace_type='cli')
        logging.info(f"Device {self.host} access in config mode")

    @__auto_login
    def user_mode(self) -> None:
        """用户特权模式， 默认进入就是用户特权模式

        :return:
        """
        self.tn.write(("\003" + "\r").encode("cp936"))
        time.sleep(1)
        read_contents = self.tn.read_very_eager().decode('cp936').strip()
        logging.debug(read_contents)
        switch_mode = None
        if self.config_tag in read_contents:
            switch_mode = 'config_mode'
        elif self.user_tag in read_contents:
            pass
        elif self.normal_tag in read_contents:
            switch_mode = 'normal_mode'
        elif self.factory_tag in read_contents:
            switch_mode = 'factory_mode'
        elif re.search(self.super_tag, read_contents):
            switch_mode = 'super_mode'
        else:
            logging.warning(f'not support this mode. telnet return contents: {read_contents}')
            self.close()
            self.__login()
            self.user_mode()
        if switch_mode:
            self.send_cli(self.__get_mode_switch_cli(self.setting.get(switch_mode).get('user_mode')),
                          key_replace={'super_user': self.super_user, 'super_password': self.super_password,
                                       'pwd': self.password, 'factory_user': self.factory_username,
                                       'factory_password': self.factory_password}, key_replace_type='cli')
        logging.info(f"Device {self.host} access in user mode")

    @__auto_login
    def normal_mode(self) -> None:
        """普通模式

        :return:
        """
        self.tn.write(("\003" + "\r").encode("cp936"))  # 普通模式下输入ctrl+c会返回  % Command is not supported!
        time.sleep(1)
        read_contents = self.tn.read_very_eager().decode('cp936').strip()
        logging.debug(read_contents)
        switch_mode = None
        if self.config_tag in read_contents:
            switch_mode = 'config_mode'
        elif self.user_tag in read_contents:
            switch_mode = 'user_mode'
        elif self.normal_tag in read_contents:
            pass
        elif self.factory_tag in read_contents:
            switch_mode = 'factory_mode'
        elif re.search(self.super_tag, read_contents):
            switch_mode = 'super_mode'
        else:
            logging.warning(
                f'not support this mode. telnet return contents: {read_contents} normal_tag: {self.normal_tag}')
            self.close()
            self.__login()
            self.normal_mode()
        if switch_mode:
            self.send_cli(self.__get_mode_switch_cli(self.setting.get(switch_mode).get('normal_mode')),
                          key_replace={'super_user': self.super_user, 'super_password': self.super_password,
                                       'pwd': self.password, 'factory_user': self.factory_username,
                                       'factory_password': self.factory_password}, key_replace_type='cli')
        logging.info(f"Device {self.host} access in normal mode")

    @__auto_login
    def factory_mode(self) -> None:
        """工厂模式， 仅部分机型支持该模式，使用时需注意

        :return:
        """
        if not self.factory_username or not self.factory_password:
            logging.exception(f"sure this device support factory mode, and init factory_username、factory_password")
            raise Exception("sure this device support factory mode, and init factory_username、factory_password")
        self.tn.write(("\003" + "\r").encode("cp936"))
        time.sleep(1)
        read_contents = self.tn.read_very_eager().decode('cp936').strip()
        logging.debug(read_contents)
        switch_mode = None
        if self.config_tag in read_contents:
            switch_mode = 'config_mode'
        elif self.user_tag in read_contents:
            switch_mode = 'user_mode'
        elif self.normal_tag in read_contents:
            switch_mode = 'normal_mode'
        elif self.factory_tag in read_contents:
            pass
        elif re.search(self.super_tag, read_contents):
            switch_mode = 'super_mode'
        else:
            logging.warning(f'not support this mode. telnet return contents: {read_contents}')
            self.close()
            self.__login()
            self.factory_mode()
        if switch_mode:
            self.send_cli(self.__get_mode_switch_cli(self.setting.get(switch_mode).get('factory_mode')),
                          key_replace={'super_user': self.super_user, 'super_password': self.super_password,
                                       'pwd': self.password, 'factory_user': self.factory_username,
                                       'factory_password': self.factory_password}, key_replace_type='cli')
        logging.info(f"Device {self.host} access in factory mode")

    @__auto_login
    def send_cli(self, command: list or str, read_until=None, type_=None, **kwargs) -> str:
        """发送命令，支持多条，返回最后一条命令输入后的结果

        :param command: 支持发送多条命令["first_command", "second_command"] or 'command'
        :param read_until: str or list, 直至返回结果终止， 与command相呼应，如None的情况表示输入命令后等待1s， ['/www', None]
        :param type_: 'super'|'config'|'user'|'normal'|'factory'|None
        :param kwargs
               timeout: 当有read_until时， timeout参数生效， 读取超时时间 默认30秒
               key_replace: 字典, 需将固定字符替换为另一字符则填写该参数, 例: {'\r\n': '', ' ': ''}等
               key_replace_type: 'cli'|'last_read'|'cli_last_read'，仅在key_replace 有值时生效，默认last_read
                                 'cli': 仅替换发出去的命令
                                 'last_read': 仅替换最后读取到的内容
                                 'cli_last_read': 既要替换cli 也要替换最后读取到的内容
               interface_replace_type: 'cli'|'last_read'|'cli_last_read'，仅在interface_replace 有值时生效，默认cli
                                 'cli': 仅替换发出去的命令
                                 'last_read': 仅替换最后读取到的内容
                                 'cli_last_read': 既要替换cli 也要替换最后读取到的内容
               read_until_timeout_no_raise: bool, 读取超时时是否抛出异常，默认False
               read_content_decode: str, 读取内容的解码方式，默认cp936

        :return: 读取超时时返回Exception， 如果命令执行正确，返回最后一条命令输入后的结果
        """
        interface_replace_type = kwargs.get('interface_replace_type') if kwargs.get('interface_replace_type') else 'cli'
        key_replace_type = kwargs.get('key_replace_type') if kwargs.get('key_replace_type') else 'last_read'
        read_content_decode = kwargs.get('read_content_decode') if kwargs.get('read_content_decode') else 'cp936'
        if kwargs.get('key_replace') and 'cli' in key_replace_type:  # 替换方法的关键字
            command = replace_str(command, kwargs.get('key_replace'))
        if self.interface_replace and 'cli' in interface_replace_type:  # 替换接口的关键字
            command = replace_str(command, self.interface_replace)
        timeout = kwargs.get('timeout') if kwargs.get('timeout') else 30
        result = ''
        if type_ == 'super':
            self.super_mode()
        elif type_ == 'config':
            self.config_mode()
        elif type_ == 'user':
            self.user_mode()
        elif type_ == 'normal':
            self.normal_mode()
        elif type_ == 'factory':
            self.factory_mode()
        logging.info(f"Device {self.host} send cli {command}")
        if command:
            command = [command] if isinstance(command, str) else command
            if read_until:
                read_until = [read_until] if isinstance(read_until, str) else read_until
                if len(read_until) != len(command):
                    logging.exception('The read_until params is error')
                    raise Exception('The read_until params is error')
            else:
                read_until = [None for i in range(0, len(command))]
            self.tn.read_very_eager()
            for com, read_until_ in zip(command, read_until):
                self.tn.write((com + "\n").encode("cp936"))
                until_result = []
                for i in range(0, timeout, 1):  # 30秒没有找到期望的就主动断开
                    time.sleep(1)
                    result = self.tn.read_very_eager().decode(read_content_decode, "ignore").strip().replace('\x08', '')
                    if result:
                        logging.debug(result)
                    if read_until_:
                        until_result.append(result)
                        read_all_data = ''.join(until_result).split(com)[-1]  # 去除命令
                        if isinstance(read_until_, str):
                            if re.search(read_until_, read_all_data):
                                result = read_all_data
                                break
                        elif isinstance(read_until_, list):
                            if not [read_until_one for read_until_one in read_until_ if
                                    not re.search(read_until_one, read_all_data)]:
                                result = read_all_data
                                break
                    else:
                        result = result.split(com)[-1]
                        # 如果没有readuntil 直接返回
                        break
                else:
                    self.tn.write(("\003" + "\r").encode("cp936"))
                    time.sleep(1)
                    if not kwargs.get('read_until_timeout_no_raise'):
                        logging.exception(f"Device {self.host} send cli {command} ReadUntilTimeOutError")
                        raise Exception('ReadUntilTimeOutError')
        if kwargs.get('key_replace') and 'last_read' in key_replace_type:
            result = replace_str(result, kwargs.get('key_replace'))
        if self.interface_replace and 'last_read' in interface_replace_type:  # 替换接口的关键字
            result = replace_str(result, self.interface_replace)
        return result

    @__auto_login
    def assert_cli(self, cli=None, expect=None, timeout=20, interval=5, type_='super', key_replace=None,
                   key_replace_type='last_read', interface_replace_type='cli', read_until=None,
                   read_content_decode=None) -> None:

        """在某个模式下支持输入一条或多条命令, 且支持对执行时最后一条命令返回的结果做断言
           该方法对ping tcpdump命令 无效

        :param cli: str or list, 发送的命令 一条或者多条
        :param read_until: str or list, 直至返回结果终止， 与cli相呼应，如None的情况表示输入命令后等待1s， ['/www', None]
        :param expect: str or list or dict, 一条或多条希望校验的存在的结果，如需要判断不存在时，可以使用字典{$expect: False}
                       同时校验时可以是{$expect1: True, $expect: False}, str或者list时都是判断存在
        :param timeout: 检测超时时间  秒
        :param interval: 检测间隔时间 秒
        :param type_: 'super'|'config'|'user'|'normal'|'factory'|None
        :param key_replace: 字典, 需将固定字符替换为另一字符则填写该参数, 例: {'\r\n': '', ' ': ''}等 默认去掉换行
        :param key_replace_type: 'cli'|'last_read'|'cli_last_read'，仅在key_replace 有值时生效，默认last_read
                                 'cli': 仅替换发出去的命令
                                 'last_read': 仅替换最后读取到的内容
                                 'expect': 仅替换期望校验的值
                                 'cli_last_read'|'cli_expect'|'last_read_expect' 任意两种组合
                                 'cli_expect_last_read': 既要替换cli 也要替换最后读取到的内容还有校验的值
        :param interface_replace_type: 'cli'|'last_read'|'cli_last_read'，仅在interface_replace 有值时生效，默认cli
                                 'cli': 仅替换发出去的命令
                                 'last_read': 仅替换最后读取到的内容
                                 'expect': 仅替换期望校验的值
                                 'cli_last_read'|'cli_expect'|'last_read_expect' 任意两种组合

                                 'cli_expect_last_read': 既要替换cli 也要替换最后读取到的内容还有校验的值
        :param read_content_decode: str, 读取内容的解码方式，默认cp936
        :return: None|Exception
        """

        def contain_(expect_, result_) -> bool:
            if expect_ in result_:  # 为str 时 如果在里面直接返回True
                return True
            else:
                try:
                    if len(re.findall(expect_, result_)):  # 匹配正则表达式
                        return True
                    else:
                        return False
                except Exception:
                    return False

        if key_replace is None:
            key_replace = {'\r\n': ''}
        if cli is not None:
            for i in range(0, timeout, interval):
                if key_replace and 'cli' in key_replace_type:
                    cli = replace_str(cli, key_replace)
                    key_replace_type = key_replace_type.replace('cli', '')
                result = self.send_cli(cli, read_until, type_=type_, key_replace=key_replace,
                                       key_replace_type=key_replace_type, read_content_decode=read_content_decode,
                                       interface_replace_type=interface_replace_type)
                expect = str(expect) if isinstance(expect, int) else expect
                check_ = True
                if expect:
                    if 'expect' in key_replace_type:
                        expect = replace_str(expect, key_replace)
                    if 'expect' in interface_replace_type:
                        expect = replace_str(expect, self.interface_replace)
                    logging.debug(f'start assert cli expect {expect}')
                    if isinstance(expect, str):
                        if not contain_(expect, result):
                            check_ = False
                    elif isinstance(expect, list):
                        if [expect_ for expect_ in expect if not contain_(expect_, result)]:
                            check_ = False
                    elif isinstance(expect, dict):
                        for k, v in expect.items():
                            if v:
                                if not contain_(k, result):
                                    check_ = False
                                    break
                            else:
                                if contain_(k, result):
                                    check_ = False
                                    break
                    else:
                        logging.exception(f'parameter expect type error, expect {expect}')
                        raise Exception('parameter expect is error')
                if check_:
                    break
                else:
                    time.sleep(interval)
                    logging.info(f"{expect} assert failure, wait for {interval}s inspection")
            else:
                logging.exception(f'{expect} not found timeout')
                raise Exception(f'{expect} not found timeout')
            logging.info(f'assert cli success')

    @__auto_login
    @loop_inspector('Telnet ping')
    def ping(self, address='www.baidu.com', packets_number=4, params='', key_replace=None, lost_packets=False,
             timeout=30, interval=5) -> bool:
        """设备里面ping地址

        :param address: 域名或者IP
        :param packets_number, ping 包的个数，默认都是4个
        :param params: 参数 如'-I cellular1'、'-s 32'
        :param key_replace: 字典类型， 传入的参数转换关系表{$old: $new}
        :param lost_packets: True|False 如果为True判断会丢包，如果为False判断不丢包
        :param timeout: 检测超时时间  秒
        :param interval: 检测间隔时间 秒
        :return:
        """
        self.super_mode()
        params = params if params.startswith(' ') else ' ' + params
        x = True
        result = self.send_cli("ping " + address + params + f' -c {packets_number}', self.super_tag,
                               key_replace=key_replace, key_replace_type='cli', )
        if lost_packets:
            # 判断需要丢包
            if 'received, 0% packet loss' in result:
                x = False
        else:
            # 当判断不为丢包时
            if 'received, 0% packet loss' not in result:
                x = False
        return x

    @__auto_login
    def tcpdump(self, expect: str or list or dict, key_replace=None, timeout=30, interval=5, **kwargs) -> None:
        """

        :param expect: str or list or dict,
                       一条或多条希望校验的存在的结果，如需要判断不存在时，可以使用字典{$expect: False}
                       str或者list时都是判断存在
        :param kwargs: 命令参数, str, interface| param| cat_num
                        interface: 接口名称, wan| wifi_24g| wifi_5g| lan| cellular1
                        param: 抓包过滤关键字, None, 'icmp', 'http', 'port 21', 'host 1.1.1.1 and icmp'
                        catch_num: 抓包数量, int
                        key_replace_type: 替换类型, str,  默认是cli
        :param key_replace: 字典类型， 传入的参数转换关系表{$old: $new}
        :param timeout: 校验超时时间, int
        :param interval: 5
        :return:
        """
        flag = {'interface': '-i', 'param': '', 'catch_num': '-c'}
        command = 'tcpdump'
        if kwargs:
            for k, v in kwargs.items():
                for k_, v_ in flag.items():
                    if k == k_:
                        command = command + f' {v_} ' + f'{v}'
        for i in range(0, timeout, interval):
            result = True
            not_expect_ = []
            if isinstance(expect, dict):
                not_expect_ = [k for k, v in expect.items() if not v]
                expect_ = [k for k, v in expect.items() if v]
            elif isinstance(expect, str):
                expect_ = [expect]
            elif isinstance(expect, list) or isinstance(expect, tuple):
                expect_ = expect
            else:
                logging.exception('parameter expect type error')
                raise Exception('parameter expect type error')
            if expect_:
                try:
                    _result = self.send_cli(command, [expect_], timeout=timeout, type_='super', key_replace=key_replace,
                                            key_replace_type=kwargs.get('key_replace_type', 'cli'), )
                    logging.debug('find the exception in tcpdump result.')
                    self.tn.write(("\003" + "\r").encode("cp936"))
                    if not_expect_:
                        if [not_expect for not_expect in not_expect_ if not_expect in _result]:
                            result = False
                except:
                    result = False
            else:
                if not_expect_:
                    _result = self.send_cli(command, '你还好', timeout=timeout, type_='super',
                                            key_replace=key_replace,
                                            key_replace_type=kwargs.get('key_replace_type', 'cli'),
                                            read_until_timeout_no_raise=True)
                    if [not_expect for not_expect in not_expect_ if not_expect in _result]:
                        result = False
            if result:
                break
            else:
                time.sleep(interval)
        else:
            logging.exception('TcpdumpTimeOutError')
            raise Exception('TcpdumpTimeOutError')

    @__auto_login
    @loop_inspector('Telnet regular match content')
    def re_match(self, command: str or list, regular: str or list, type_='super',
                 key_replace=None, key_replace_type='last_read', timeout=20, interval=5) -> str or List[str]:
        """根据表达式获取最后一次执行命令的匹配值

        :param command: 发送命令，可以是一条或多条
        :param regular: 正则表达式，对执行的最后一次命令返回内容进行正则查询，必须要查询到，
                        如果查不到，直至查询超时并报错
                        如果查到不止一个，返回每个正则表达式的第一个
                        列子：硬件地址 r'HWaddr(.*)inet6'， '(([0-9a-fA-F]{2}[:]){5}([0-9a-fA-F]{2})|([0-9a-fA-F]{2}[-]){5}([0-9a-fA-F]{2}))'
        :param type_: 'super'|'config'|'user'|'normal'|'factory'|None
        :param key_replace: dict 替换最后一次命令返回内容的值 默认：{'\r\n':'', ' ': ''}
        :param key_replace_type: 'cli'|'last_read'|'cli_last_read'，仅在key_replace 有值时生效，默认last_read
                                 'cli': 仅替换发出去的命令
                                 'last_read': 仅替换最后读取到的内容
                                 'cli_last_read': 既要替换cli 也要替换最后读取到的内容
        :param timeout: 超时时间 s
        :param interval: 检测间隔时间 s
        :return: str or list ，根据正则表达式的个数返回值
        """
        key_replace = {'\r\n': '', ' ': ''} if key_replace is None else key_replace
        key_replace_type = 'last_read' if key_replace_type is None else key_replace_type
        result = self.send_cli(command, type_=type_, key_replace=key_replace, key_replace_type=key_replace_type)
        if isinstance(regular, str):
            re_list = re.findall(regular, result)
            if re_list:
                for i in re_list:
                    if isinstance(i, str):
                        return re.findall(regular, result)[0]
                    else:
                        return re.findall(regular, result)[0]
            else:
                logging.debug(f'regular {regular} match content None')
                return False
        elif isinstance(regular, list):
            result_ = []
            for regular_ in regular:
                re_list = re.findall(regular_, result)
                if re_list:
                    for i in re_list:
                        if isinstance(i, str):
                            result_.append(re.findall(regular_, result)[0])
                        else:
                            result_.append(re.findall(regular_, result)[0][0])
                else:
                    logging.debug(f'regular {regular_} match content None')
                    return False
            else:
                return result_

    # intools 实现获取信息更改信息
    @__auto_login
    def in_tools(self, get_info: str or list) -> str or List[str] or None:
        """在超级模式下可以获取或者设置相关intools的属性

        :param get_info: 常用属性可能会有productnumber,oem_name,等intools里面的属性
                       列： get_info='productnumber'，需要获取多个属性时采用列表传入

        :return: 返回需要获取的信息
        """
        if get_info:
            if isinstance(get_info, str):
                regular = f'{get_info}=(.*)\\r\\n'
            else:
                regular = [f'{info}=(.*)\\r\\n' for info in get_info]
            return self.re_match('intools', regular, key_replace={})

    @__auto_login
    def kill_process(self, name: str) -> None:
        """使用kill杀死对应进程

        :param name: 进程相关名称
        :return:
        """
        self.send_cli(f'killall -9 {name}', type_='super')

    @__auto_login
    def reboot(self) -> None:
        """直接重启设备

        @return:
        """
        self.user_mode()
        self.send_cli(['reboot', 'y'])
        logging.info("【%s】Device is rebooting, wait for moment" % self.host)
        time.sleep(30)
        for i in range(0, 150, 5):
            try:
                d = telnetlib.Telnet(self.host, self.port, timeout=1)
                logging.info("【%s】Device reboot success" % self.host)
                d.close()
                break
            except Exception:
                time.sleep(5)
                pass

    @__auto_login
    def close(self) -> None:
        """关闭连接

        @return:
        """
        self.tn.close()
        logging.info("Telnet 【%s:%s】 close connect session" % (self.host, self.port))

    @__auto_login
    def connect_aws(self, platform='star.inhandcloud.cn'):
        """通过设备后台切换平台
        :param platform: 'star.nezha.inhand.dev'|'star.inhandcloud.cn'|'star.nezha.inhand.design'|'star.inhandcloud.com'|'beta.star.inhand.design'

        """
        if self.model not in ['ER805', 'ER605', 'ODU2002', 'IR624', 'ER2000', 'FWA02']:
            raise Exception('This model not support, please check')
        awscloud_path = {'er605': '/var/backups/awscloud.json', 'er805': '/tmp/backups/awscloud.json',
                         'odu2002': '/var/backups/awscloud.json', 'ir624': '/var/backups/awscloud.json',
                         'fwa02': '/tmp/backups/awscloud.json'}.get(self.model.lower())
        self.super_mode()
        # 使用echo命令直接覆盖原文件内容
        command = 'echo -e \'{\n"server": "' + platform + '",\n"keepalive": 60\n}\'  > ' + awscloud_path
        self.send_cli({command: "/www #"})
        self.kill_process('NetworkManager')

    @__auto_login
    def enable_wan_telnet(self) -> None:
        """开启wan口telnet

        :return:
        """
        if self.model not in ['ER805', 'ER605', 'ODU2002', 'IR624', 'ER2000']:
            raise Exception('This model not support, please check')
        self.send_cli('iptables -A PERMIT-SERVICE -p tcp -m tcp --dport 23 -j ACCEPT', type_='super')


if __name__ == '__main__':
    from inhandtest.log import enable_log

    enable_log('./log.log', 'DEBUG')
    a = Telnet('ER805', '192.168.2.1', connect_timeout=20, connect_interval=5)
    # a.super_mode()
    a.connect_aws('star.inhandcloud.cn')
    # a.assert_cli('ifconfig', 'fe80::67f:eff:fe01:92be/64')
