#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2019/3/16
@Author  : wangjh
@desc    : PyCharm
"""


def save_source(filename, content):
    with open(filename, 'w', encoding='utf-8')as f:
        f.write(content)
        return


def read_source(filename):
    with open(filename, 'r', encoding='utf-8')as f:
        content = f.read()
        return content
