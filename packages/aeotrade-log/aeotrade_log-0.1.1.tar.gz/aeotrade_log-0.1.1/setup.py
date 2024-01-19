"""
@company: 慧贸天下(北京)科技有限公司
@author: wanghao@aeotrade.com
@time: 2024/1/5 14:57 
@file: setup.py.py
@project: aeotrade_log
@describe: None
"""
from setuptools import setup, find_packages

setup(
    name="aeotrade_log",
    version="0.1.1",
    author="Hero",
    author_email="wanghao@aeotrade.com",
    description="log config",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
