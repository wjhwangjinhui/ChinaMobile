#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2019/3/16
@Author  : wangjh
@desc    : PyCharm
"""
import ast
import os
import random
import time
from lxml import etree
from PIL import Image
from base.handle_redis import HandleRedis
from get_source.captcha_method import Recognize
from mylog import log

fir_dir = os.path.abspath(os.path.dirname(__file__))
filedir = os.path.join(fir_dir, 'captcha')

r = Recognize()
hr = HandleRedis(5)


def data_to_redis(task_id, data):
    table = task_id
    hr.cache_str_redis(table, data)


def get_info(task_id):
    data = hr.get_data_redis2(task_id)
    return ast.literal_eval(data.decode())


def captcha():
    """
    使用打码平台识别验证码
    :return:
    """
    filename = 'yzm.png'
    img = os.path.join(filedir, filename)
    result, pic_id = r.recognize_captcha(img, 1006)
    return result, pic_id


def get_screen_shot():
    """
    将保存下来的图片切割出验证图片
    :return:
    """
    file1 = 'screen.png'
    file2 = 'yzm.png'
    file_name = os.path.join(filedir, file1)
    im = Image.open(file_name)
    im = im.crop((640, 337, 800, 407))
    im.save(os.path.join(filedir, file2))


def get_cap(browser):
    vec_imgcode = browser.find_element_by_id('vec_imgcode')
    # 另外的一个页面打开验证码url
    js = 'window.open("https://shop.10086.cn/i/authImg?t={}");'.format(random.random())
    browser.execute_script(js)
    time.sleep(1)
    home_handles = browser.current_window_handle  # 获取主页面的句柄
    handles = browser.window_handles  # 获取所有的句柄
    use_handles = None
    for handle in handles:
        if handle != home_handles:
            use_handles = handle
    browser.switch_to.window(use_handles)
    file1 = 'screen.png'
    file_name = os.path.join(filedir, file1)
    browser.get_screenshot_as_file(file_name)  # 保存浏览器页面
    browser.close()  # 关闭新开验证码窗口
    browser.switch_to.window(home_handles)  # 切回到主页面
    get_screen_shot()  # 将保存的浏览器图片切割成标准验证码图片
    result, pic_id = captcha()  # 返回识别的验证码
    log.crawler.info('输入验证码')
    vec_imgcode.send_keys(result)  # 输入图片验证码
    time.sleep(5)
    # WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.ID, "detailerrmsg")))
    html = browser.page_source
    tree = etree.HTML(html)
    interstat = tree.xpath('//*[@id="undefined"]/table/tbody/tr[5]/td[2]/input/@interstat')[0]
    # ms = browser.find_elements_by_xpath('//*[@id="detailerrmsg"]')[0].text
    # log.crawler.info('interstat为{}'.format(interstat))
    # if ms == '验证码错误，请重新输入':
    if str(interstat) == "1":
        file1 = str(result) + '.png'
        file_name = os.path.join(filedir, file1)
        im = Image.open(os.path.join(filedir, 'yzm.png'))
        im = im.crop()
        im.save(file_name)
    else:
        vec_imgcode.clear()
        r.report_err(pic_id)
        get_cap(browser)


if __name__ == '__main__':
    data = {
        'phone_num': '',
        'serverpwd': '',
        'smspwd': '700'
    }
    data_to_redis(data)
    # a = get_info()
    # print(type(a))
    # captcha()
    # get_screen_shot()
