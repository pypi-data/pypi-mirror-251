#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
author：yannan1
since：2023-09-20
"""

from setuptools import setup

setup(
    name='visioncube',
    packages=[
        'visioncube',
        'visioncube.functional',
        'visioncube.functional_cuda',
        'visioncube.operators',
        'visioncube.operators_cuda',
    ],
    version='0.2.1',
    description='Image Processing Tool',
    author='yanaenen, xi',
    install_requires=[
        'numpy',
        'imgaug',
        'opencv-python',
        'torch',
        'kornia',
        'torchvision',
        'PyYAML',
        'matplotlib',
    ],
    platforms='any',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    include_package_data=True,
    zip_safe=False,
)
