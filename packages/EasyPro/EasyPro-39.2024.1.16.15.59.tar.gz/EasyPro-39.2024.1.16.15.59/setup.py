# -*- coding:utf-8 -*-
import sys
sys.argv.append('sdist')
from distutils.core import setup
from setuptools import find_packages

setup(name='EasyPro',
            version='39.2024.1.16.15.59',
            packages=['EasyPro',],
            description='A python lib for xxxxx',
            long_description='',
            author='Quanfa',
            package_data={
            '': ['*.*'],
            },
            author_email='quanfa@tju.edu.cn',
            url='http://www.xxxxx.com/',
            license='MIT',
            )

            