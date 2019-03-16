#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2019/3/16
@Author  : wangjh
@desc    : PyCharm
"""
import datetime
from dateutil.relativedelta import relativedelta


def get_time():
    datetime_now = datetime.datetime.now()
    datetime_month_ago = datetime_now - relativedelta(months=6)
    a = datetime_month_ago.strftime('%Y%m')
    first_time = a + '01'
    last_time = datetime_now.strftime('%Y%m%d')
    return (first_time, last_time)


def get_month(i):
    datetime_now = datetime.datetime.now()
    datetime_month_ago = datetime_now - relativedelta(months=i - 1)
    month = datetime_month_ago.strftime('%Y-%m')
    return month


if __name__ == '__main__':
    # a = get_time()
    # print(a)
    # a = get_month(i=7)
    # print(a)
    datetime_now = datetime.datetime.now()
    datetime_month_ago = datetime_now - relativedelta(months=1)
    month = datetime_month_ago.strftime('%Y-%m')
    print(month)
