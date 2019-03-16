#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2019/3/16
@Author  : wangjh
@desc    : PyCharm
"""
import datetime
import os
import re

from lxml import etree
from get_source.io_source import read_source

fir_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
filedir = os.path.join(fir_dir, 'html_source')


def get_home(task_id):
    file_name = os.path.join(filedir, str(task_id) + '\\' + 'home.html')
    content = read_source(file_name)
    tree = etree.HTML(content)
    use_mon = tree.xpath('//*[@id="stc_myaccount"]/div/div/div[1]/p/span[1]/text()')[0]
    all_mon = tree.xpath('//*[@id="stc_myaccount"]/div/div/div[2]/p/span[1]/text()')[0]
    used_mon = tree.xpath('//*[@id="stc_myaccount"]/div/div/div[3]/p/span[1]/text()')[0]
    point = tree.xpath('//*[@id="stc_myaccount"]/div/div/div[4]/p/span[1]/text()')[0]
    a = tree.xpath('//*[@id="stc_packramin"]/div[1]/span[3]/text()')[1]
    b = tree.xpath('//*[@id="stc_packramin"]/div[1]/span[3]/span/text()')[0]
    c = tree.xpath('//*[@id="stc_packramin"]/div[2]/span[3]/text()')[1]
    d = tree.xpath('//*[@id="stc_packramin"]/div[2]/span[3]/span/text()')[0]

    data = {
        'use_mon': use_mon,
        'all_mon': all_mon,
        'used_mon': used_mon,
        'point': point,
        'speech': b + a,
        'gprs': d + c
    }
    return data


if __name__ == '__main__':
    a = get_home()
    print(a)
