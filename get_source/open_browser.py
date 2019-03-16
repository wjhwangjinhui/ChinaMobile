#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2019/3/16
@Author  : wangjh
@desc    : PyCharm
"""
import random

from selenium import webdriver


def get_browser():
    # options = webdriver.ChromeOptions()
    # options.add_argument('disable-infobars')
    browser = webdriver.Chrome(executable_path=r'D:\work_space\ChinaMobile\get_source\chromedriver.exe')
    return browser


if __name__ == '__main__':
    browser = get_browser()
    browser.maximize_window()
    img_url = 'https://shop.10086.cn/i/authImg?t={}'.format(random.random())
    browser.get(img_url)

    browser.get_screenshot_as_file(r'C:\Users\wangjh\Desktop\ChinaMobile\get_source\captcha\qwe.png')
