# -*- coding: utf-8 -*-

# ------------------------------
# @Time    : 2024/1/18
# @Author  : gao
# @File    : setup.py
# @Project : AmazingData
# ------------------------------

from setuptools import setup, find_packages

setup(
    name='AmazingData',  # 包名
    version='0.0.3',  # 包的版本号
    description='AmazingData',  # 包的描述信息
    author='Your gao',  # 作者
    author_email='your_email@example.com',  # 作者邮箱
    url='https://gitee.com/zhanggao2013/AmazingData', # 包的代码仓库地址
    packages=find_packages(),  # 包含的包
    classifiers=[  # 包的分类
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8',
    ],
)
