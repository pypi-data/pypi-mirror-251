#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from setuptools import setup, find_packages

# setup.py
# Created by fzhiheng on 2024/1/16
# Copyright (c) 2024 fzhiheng. All rights reserved.
# 2024/1/16 上午9:35

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="pyrotation",
      version="0.1",
      description="A package to handle rotation in 3D space with pytorch and numpy",
      long_description=long_description,
      ong_description_content_type="text/markdown",
      classifiers=[
          "Intended Audience :: Science/Research",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
      ],
      keywords="rotation transformations quaternions euler angles axis angle",
      url="https://github.com/fzhiheng/pyrotation.git",
      author="fzhiheng",
      author_email="fzhazr@sjtu.edu.cn",
      license="MIT",
      packages=find_packages(),
      install_requires=["numpy", "torch", "plum-dispatch"],
      include_package_data=True,
      zip_safe=False,
      )
