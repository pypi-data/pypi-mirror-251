# -*- coding: utf-8 -*-
# @Time    : 2023/1/31 16:47:12
# @Author  : Pane Li
# @File    : setup.py
"""

setup

"""
from distutils.core import setup
from setuptools import find_packages

# 读取requirements 文件中的库，并生成一个列表
require_list = open('requirements.txt', 'r', encoding='utf-8').readlines()
require_list = [i.strip() for i in require_list]

setup(
    name='inhandtest',
    version='0.0.81',
    author='liwei',
    author_email='liwei@inhand.com.cn',
    description='inhand test tools, so easy',
    maintainer='liwei',
    maintainer_email='liwei@inhand.com.cn',
    # py_modules=['inhandtest.tools', 'inhandtest.telnet', 'inhandtest.inmodbus', 'inhandtest.inmqtt', 'inhandtest.file',
    #             'inhandtest.inrequest', 'inhandtest.inssh', 'inhandtest.base_page'],
    # packages=['inhandtest', 'inhandtest.base_page', 'inhandtest.pages', 'inhandtest.pages.ingateway', ],
    packages=find_packages(),
    package_data={'inhandtest': ['*.html', '*.yaml'], 'inhandtest.pages.ingateway': ['*.yml'],
                  'inhandtest.base_page': ['*.yaml']},
    url='https://inhandnetworks.yuque.com/irhb08/mrpu1r/qgu0imvigkm2xry9?singleDoc# 《inhandtest docs》',
    long_description='方便inhand测试同事在自动化测试时，对通用协议或者常用工具及方法做封装，需要使用时即在线安装；\n映翰通出品，追尾必究！',
    classifiers=[
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=require_list,
)
