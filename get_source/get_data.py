#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2019/3/16
@Author  : wangjh
@desc    : PyCharm
"""
import os
import time

from get_source.com import get_time
from get_source.io_source import save_source
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from get_source.user_login_info import get_info, get_cap, data_to_redis
from mylog import log

fir_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
filedir = os.path.join(fir_dir, 'html_source')


def switch_window(browser):
    home_handles = browser.current_window_handle  # 获取主页面的句柄
    handles = browser.window_handles  # 获取所有的句柄
    use_handles = None
    for handle in handles:
        if handle != home_handles:
            use_handles = handle
    browser.switch_to.window(use_handles)
    info = browser.page_source
    browser.close()
    browser.switch_to.window(home_handles)
    return info


# 个人信息
def get_user_info(browser, phone_num, task_id):
    js = 'window.open("https://shop.10086.cn/i/v1/cust/info/{}?_={}");'.format(phone_num, (int(time.time() * 1000)))
    browser.execute_script(js)
    time.sleep(1)
    info1 = switch_window(browser)
    file1 = str(task_id) + '\\' + 'info1.html'
    file_name = os.path.join(filedir, file1)
    save_source(file_name, info1)
    js = 'window.open("https://shop.10086.cn/i/v1/busi/plan/{}?_={}");'.format(phone_num, (int(time.time() * 1000)))
    browser.execute_script(js)
    time.sleep(1)
    info2 = switch_window(browser)
    file2 = str(task_id) + '\\' + 'info2.html'
    file_name = os.path.join(filedir, file2)
    save_source(file_name, info2)


# 流量
def get_user_gprs(browser, phone_num, task_id):
    js = 'window.open("https://shop.10086.cn/i/v1/fee/planbal/{}?_={}");'.format(phone_num, (int(time.time() * 1000)))
    browser.execute_script(js)
    time.sleep(1)
    gprs = switch_window(browser)
    file = str(task_id) + '\\' + 'gprs.html'
    file_name = os.path.join(filedir, file)
    save_source(file_name, gprs)


# 缴费记录  替换时间时间(1个月，3个月，6个月，12个月)  后加时间戳
def get_user_count(browser, phone_num, task_id):
    dt = get_time()
    js = 'window.open("https://shop.10086.cn/i/v1/cust/his/{}?startTime={}&endTime={}&_={}");'.format(
        phone_num, dt[0], dt[1], (int(time.time() * 1000)))
    browser.execute_script(js)
    time.sleep(1)
    count = switch_window(browser)
    file = str(task_id) + '\\' + 'count.html'
    file_name = os.path.join(filedir, file)
    save_source(file_name, count)


# 账单 近一年
def get_user_bill(browser, phone_num, task_id):
    js = 'window.open("https://shop.10086.cn/i/v1/fee/billinfo/{}?_={}");'.format(phone_num, (int(time.time() * 1000)))
    browser.execute_script(js)
    time.sleep(1)
    bill = switch_window(browser)
    file = str(task_id) + '\\' + 'bill.html'
    file_name = os.path.join(filedir, file)
    save_source(file_name, bill)


def get_smspwd(task_id):
    t1 = time.time()
    while True:
        data = get_info(task_id)
        smspwd = data['smspwd']
        if smspwd:
            return smspwd
        else:
            t2 = time.time()
            if int(t2 - t1) > 50:
                return ''


def yan(browser, task_id, tag):
    tag.click()
    time.sleep(3)
    try:
        vec_servpasswd = browser.find_element_by_id('vec_servpasswd')
    except:
        vec_servpasswd = ''
    if vec_servpasswd:
        vec_servpasswd = browser.find_element_by_id('vec_servpasswd')
        data = get_info(task_id)
        serverpwd = data['serverpwd']
        vec_servpasswd.send_keys(serverpwd)  # 输入服务密码
        stc_send_sms = browser.find_element_by_id('stc-send-sms')
        stc_send_sms.click()
        time.sleep(0.8)
        alert = browser.switch_to.alert  # 页面弹窗按确定
        alert.accept()
        log.crawler.info('获取随机码')
        data['status_code'] = 2003
        data_to_redis(task_id, data)
        vec_smspasswd = browser.find_element_by_id('vec_smspasswd')
        smspwd = get_smspwd(task_id)  # 输入手机验证码
        if smspwd:
            vec_smspasswd.send_keys(smspwd)
        else:
            time.sleep(20)
            # 第二次获取随机码
            stc_send_sms.click()
            time.sleep(2)
            alert = browser.switch_to.alert  # 页面弹窗按确定
            alert.accept()
            log.crawler.info('第二次获取随机码')
            data['status_code'] = 2003
            data_to_redis(task_id, data)
            smspwd = get_smspwd(task_id)
            vec_smspasswd.send_keys(smspwd)  # 输入手机验证码
        get_cap(browser)
        WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.ID, "vecbtn")))
        vecbtn = browser.find_element_by_id('vecbtn')
        vecbtn.click()
        time.sleep(1)
        data['smspwd'] = ''
        data_to_redis(task_id, data)
        ms = browser.find_elements_by_xpath('//*[@id="detailerrmsg"]')
        time.sleep(1)
        if ms:
            a = ms[0].text
            if a == '随机密码错误!':
                log.crawler.info('随机密码错误!')
                data['status_code'] = 2006
                data_to_redis(task_id, data)
            else:
                log.crawler.info('服务密码错误')
                data['status_code'] = 1003
                data_to_redis(task_id, data)
            cut = browser.find_elements_by_xpath('//*[@id="undefined"]/span')[0]
            cut.click()
            yan(browser, task_id, tag)


# 详细账单
def get_detail_data(browser, task_id):
    time.sleep(7)
    detiail_tag = browser.find_elements_by_xpath('//*[@id="stcnavmenu"]/ul[2]/li/ul/li[4]/a')[0]
    detiail_tag.click()
    WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.ID, "month1")))
    li = browser.find_elements_by_xpath('//*[@id="month1"]')[0]
    # WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "vec_servpasswd")))
    log.crawler.info('详情页验证码')
    yan(browser, task_id, li)
    data = get_info(task_id)
    data['status_code'] = 2000
    data_to_redis(task_id, data)
    log.crawler.info('鉴权成功')


# '套餐及固定费', '通话详单', '短信详单'
def get_plan_amt(browser, task_id):
    for i in [1, 2, 4]:
        title = browser.find_elements_by_xpath('//*[@id="switch-data"]/li[{}]/p'.format(i))[0]
        yan(browser, task_id, title)
        for j in range(1, 7):
            a = 'month' + str(j)
            month = browser.find_elements_by_xpath('//*[@id="{}"]'.format(a))[0]
            yan(browser, task_id, month)
            data = get_info(task_id)
            data['status_code'] = 3000
            data_to_redis(task_id, data)
            time.sleep(1)
            source = browser.page_source
            title_list = ['套餐及固定费', '通话详单', '上网详单', '短信详单']
            file = str(task_id) + '\\' + title_list[i - 1] + a + '_1' + '.html'
            file_name = os.path.join(filedir, file)
            save_source(file_name, source)
            b = browser.find_elements_by_xpath('//*[@id="notes1"]')
            if b:
                c = b[0].text
                # a = '第1/1页'
                pages = c.split('/')[1].split('页')[0]
                if int(pages) > 1:
                    for k in range(2, int(pages) + 1):
                        time.sleep(1)
                        next = browser.find_element_by_class_name('next')
                        yan(browser, task_id, next)
                        data = get_info(task_id)
                        data['status_code'] = 3000
                        data_to_redis(task_id, data)
                        time.sleep(1)
                        source = browser.page_source
                        file = str(task_id) + '\\' + title_list[i - 1] + a + '_' + str(k) + '.html'
                        file_name = os.path.join(filedir, file)
                        save_source(file_name, source)
                else:
                    pass
            else:
                pass
