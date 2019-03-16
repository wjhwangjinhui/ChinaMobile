#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2019/3/16
@Author  : wangjh
@desc    : PyCharm
"""
import os
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from get_source.io_source import save_source
from get_source.user_login_info import get_info, data_to_redis
from mylog import log

fir_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
filedir = os.path.join(fir_dir, 'html_source')


# 服务密码登录 待修改(有时要验证码，有时不需要)
def login_user_serv(browser, phone_num, ser_pwd):
    url = 'https://login.10086.cn/login.html'
    browser.get(url=url)
    time.sleep(0.6)
    p_name = browser.find_element_by_id('p_name')
    p_pwd = browser.find_element_by_id('p_pwd')
    submit_bt = browser.find_element_by_id('submit_bt')
    p_name.send_keys(phone_num)
    p_pwd.send_keys(ser_pwd)
    time.sleep(1)
    getSMSPwd = browser.find_element_by_id('getSMSPwd')
    sms_pwd = browser.find_element_by_id('sms_pwd')
    getSMSPwd.click()
    sms_pwd.send_keys(input('请输入手机验证码：'))
    submit_bt.click()
    browser.maximize_window()


def get_smspwd(task_id):
    while True:
        data = get_info(task_id)
        smspwd = data['smspwd']
        if smspwd:
            return smspwd


# 验证码登录
def login_user_cap(browser, phone_num, task_id):
    url = 'https://login.10086.cn/login.html'
    browser.get(url=url)
    browser.maximize_window()  # 窗口最大化
    WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.ID, "sms_login_1")))
    sms_login_1 = browser.find_element_by_id('sms_login_1')
    sms_login_1.click()
    WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.ID, "sms_name")))
    sms_name = browser.find_element_by_id('sms_name')
    sms_name.send_keys(phone_num)
    getSMSPwd1 = browser.find_element_by_id('getSMSPwd1')
    getSMSPwd1.click()
    smsphone_err = browser.find_element_by_id('smsphone_err')
    data = get_info(task_id)
    if smsphone_err.is_displayed():
        log.crawler.info('手机号有误')
        data['status_code'] = 1002
        data_to_redis(task_id, data)
        browser.quit()
    WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.ID, "sms_pwd_l")))
    sms_pwd_l = browser.find_element_by_id('sms_pwd_l')
    data['status_code'] = 2003
    data_to_redis(task_id, data)
    smspwd = get_smspwd(task_id)
    sms_pwd_l.send_keys(smspwd)  # 输入手机验证码
    submit_bt = browser.find_element_by_id('submit_bt')
    smspwd_err = browser.find_element_by_id('smspwd_err')
    submit_bt.click()
    time.sleep(0.2)
    if smspwd_err.is_displayed():
        log.crawler.info('请输入正确短信随机码')
        data['status_code'] = 2006
        data_to_redis(task_id, data)
    time.sleep(2)
    log.crawler.info('登陆成功')
    data['status_code'] = 1004
    data['smspwd'] = ''
    data_to_redis(task_id, data)
    time.sleep(1)
    source = browser.page_source
    file = str(task_id) + '\\' + 'home.html'
    file_name = os.path.join(filedir, file)
    save_source(file_name, source)


if __name__ == '__main__':
    pass

