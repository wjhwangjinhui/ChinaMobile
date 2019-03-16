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


def get_plan_amt(dir, phone_num):
    file_name = os.path.join(filedir, dir)
    content = read_source(file_name)
    tree = etree.HTML(content)
    tr_list = tree.xpath('//*[@id="tbody"]/tr')
    data_list = []
    for tr in tr_list:
        name = tr.xpath('./td[3]/text()')[0]
        count = tr.xpath('./td[4]/text()')[0]
        count_time = tr.xpath('./td[1]/text()')[0]
        update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cell_phone = phone_num
        data = {
            'name': name,
            'count': count,
            'count_time': count_time,
            'update_time': update_time,
            'cell_phone': cell_phone
        }
        data_list.append(data)
    return data_list


def get_transactions(task_id, m, phone_num):
    f = filedir + '\\' + str(task_id)
    dirlist = os.listdir(f)
    transactions = []
    for dir in dirlist:
        a = dir[0]
        if a == '套':
            b = re.findall("""套餐及固定费month(\d+)_\d+\.html""", dir)[0]
            if b == m:
                data = get_plan_amt(str(task_id) + '\\' + dir, phone_num)
                transactions = transactions + data
    return transactions


if __name__ == '__main__':
    pass
