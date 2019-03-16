#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2019/3/16
@Author  : wangjh
@desc    : PyCharm
"""
from get_source.com import get_month
from parse_html.parse_amt import get_home
from parse_html.parse_basic import get_info, get_count, get_bill
from parse_html.parse_calls import get_calls
from parse_html.parse_smses import get_smses
from parse_html.parse_transactions import get_transactions


def com_data(task_id, phone_num):
    basic = get_info(task_id, phone_num)
    count = get_count(task_id)
    bill = get_bill(task_id)
    try:
        home = get_home(task_id)
    except:
        home = []
    data1 = {
        "home": home,
        'basic': basic,
        'count': count,
        'bill': bill
    }
    return data1


def mobile(task_id, a, phone_num):
    calls = get_calls(task_id, a, phone_num)
    smses = get_smses(task_id, a, phone_num)
    transactions = get_transactions(task_id, a, phone_num)
    data2 = {
        'transactions': transactions,
        'calls': calls,
        'smses': smses,
    }
    return [data2]


def last_data(task_id, phone_num):
    data1 = com_data(task_id, phone_num)
    data = []
    data.append(data1)
    for i in range(1, 7):
        d = mobile(task_id, str(i), phone_num)
        month = get_month(i)
        da = {month: d}
        data.append(da)
    return data


if __name__ == '__main__':
    data = last_data('9235cdf51598d98c00c7a85a09af4809', '手机号')
    print(data)
