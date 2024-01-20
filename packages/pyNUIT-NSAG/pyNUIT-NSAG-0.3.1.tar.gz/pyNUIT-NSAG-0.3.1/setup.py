'''
Author: albertzhang albert.zhangweij@outlook.com
Date: 2023-12-22 11:20:00
Description: 

Copyright (c) 2024 by THU-RSAG, All Rights Reserved. 
'''
import setuptools

with open("README.md", "r") as fileopen:
    long_description = fileopen.read()

setuptools.setup(
    name="pyNUIT-NSAG",
    version="0.3.1",
    author="THU-RSAG",
    author_email="z-wj21@mails.tsinghua.edu.cn",
    description="Wrapper for source term alaysis code NUIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thu-inet/pyNUIT",
    packages=setuptools.find_packages(),
    install_requires=['numpy>=1.26.0', 'pandas>=2.1.3', 'matplotlib>=3.8.2'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
)
