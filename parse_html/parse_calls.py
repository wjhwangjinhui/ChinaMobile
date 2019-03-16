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
        place = tr.xpath('./td[2]/text()')[0]
        other_cell_phone = tr.xpath('./td[4]/text()')[0]
        subtotal = tr.xpath('./td[8]/text()')[0]
        start_time = tr.xpath('./td[1]/text()')[0]
        init_type = tr.xpath('./td[3]/text()')[0]
        call_type = tr.xpath('./td[6]/text()')[0]
        use_time = tr.xpath('./td[5]/text()')[0]
        update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cell_phone = phone_num
        data = {
            'place': place,
            'other_cell_phone': other_cell_phone,
            'subtotal': subtotal,
            'start_time': start_time,
            'init_type': init_type,
            'call_type': call_type,
            'use_time': use_time,
            'update_time': update_time,
            'cell_phone': cell_phone
        }
        data_list.append(data)
    return data_list


def get_calls(task_id, m, phone_num):
    f = filedir + '\\' + str(task_id)
    dirlist = os.listdir(f)
    calls = []
    for dir in dirlist:
        a = dir[0]
        if a == '通':
            b = re.findall("""通话详单month(\d+)_\d+\.html""", dir)[0]
            if b == m:
                data = get_plan_amt(str(task_id) + '\\' + dir, phone_num)
                calls = calls + data
    return calls


if __name__ == '__main__':
    pass
