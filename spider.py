#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2019/3/16
@Author  : wangjh
@desc    : PyCharm
"""


from get_source.get_data import get_user_gprs, get_user_info, get_user_count, get_user_bill, get_detail_data, \
    get_plan_amt
from get_source.login import login_user_cap
from get_source.open_browser import get_browser
from get_source.user_login_info import get_info, data_to_redis



def start_spider(phone_num, task_id):
    browser = get_browser()
    login_user_cap(browser, phone_num, task_id)  # 登录
    get_detail_data(browser, task_id)  # 详单验证
    data = get_info(task_id)
    data['status_code'] = 3000
    data_to_redis(task_id, data)
    get_plan_amt(browser, task_id)  # 详细账单
    get_user_info(browser, phone_num, task_id)  # 个人信息
    get_user_gprs(browser, phone_num, task_id)  # 流量
    get_user_count(browser, phone_num, task_id)  # 缴费记录
    get_user_bill(browser, phone_num, task_id)  # 账单



if __name__ == '__main__':
    pass
