#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2019/3/16
@Author  : wangjh
@desc    : PyCharm
"""
import datetime
import json
import os
import re
from get_source.io_source import read_source

fir_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
filedir = os.path.join(fir_dir, 'html_source')


def get_info(task_id, phone_num):
    file_name1 = os.path.join(filedir, str(task_id) + '\\' + 'info1.html')
    file_name2 = os.path.join(filedir, str(task_id) + '\\' + 'info2.html')
    info1 = read_source(file_name1)
    info2 = read_source(file_name2)
    info1 = re.findall(""";">(.*?)</""", info1)[0]
    info1 = json.loads(str(info1))
    # print('info1为：{}'.format(info1))
    info2 = re.findall(""";">(.*?)</""", info2)[0]
    info2 = json.loads(str(info2))
    # print('info2为：{}'.format(info2))
    a = info1.get('data')
    b = info2.get('data')
    intime = a.get('inNetDate', '')
    starTime = a.get('starTime', '')
    data = {}
    data['real_name'] = a.get('name', '')  # 用户名
    data['status'] = '正常' if a.get('status') == '00' else '不正常'  # 用户状态
    data['reg_time'] = intime[0:4] + '-' + intime[4:6] + '-' + intime[6:8] + ' ' + intime[8:10] \
                       + ':' + intime[10:12] + ':' + intime[12:14]  # 入网时间
    data['netAge'] = a.get('netAge', '')  # 网龄
    data['email'] = a.get('email', '')  # 邮箱
    data['address'] = a.get('address')  # 联系地址
    data['starLevel'] = a.get('starLevel', '')  # 星级
    data['starScore'] = a.get('starScore', '')  # 星级得分
    data['starTime'] = starTime[0:4] + '-' + starTime[4:6] + '-' + starTime[6:8]  # 星级有效期
    data['realNameInfo'] = '已登记' if a.get('realNameInfo', '') == '2' else '未登记'  # 实名认证
    data['brandName'] = b.get('brandName', '')  # 所属品牌
    data['curPlanName'] = b.get('curPlanName', '')  # 当前套餐
    data['idcard'] = ""
    update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cell_phone = phone_num
    data['update_time'] = update_time
    data['cell_phone'] = cell_phone
    return data


def get_gprs():
    file_name = os.path.join(filedir, 'gprs.html')
    gprs = read_source(file_name)
    gprs = re.findall(""";">(.*?)</""", gprs)[0]
    # print('gprs为：{}'.format(gprs))
    gprs_data = []
    gprs = json.loads(str(gprs))
    datas = gprs.get('data')[0].get('arr')
    for a in datas:
        mealName = a.get('mealName')
        resInfos = a.get('resInfos')[0]
        for secResInfo in resInfos.get('secResInfos'):
            b = secResInfo.get('resConInfo')
            totalMeal = b.get('totalMeal', '')
            useMeal = b.get('useMeal', '')
            balMeal = b.get('balMeal', '')
            data = {}
            data['mealName'] = mealName
            data['totalMeal'] = totalMeal
            data['useMeal'] = useMeal
            data['balMeal'] = balMeal
            gprs_data.append(data)
    return gprs_data


def get_count(task_id):
    file_name = os.path.join(filedir, str(task_id) + '/' + 'count.html')
    count = read_source(file_name)
    count = re.findall(""";">(.*?)</""", count)[0]
    # print('count为：{}'.format(count))
    gprs = json.loads(str(count))
    datas = gprs.get('data')
    count_data = []
    for a in datas:
        c_time = a.get('payDate')
        data = {}
        data['payDate'] = c_time[0:4] + '-' + c_time[4:6] + '-' + c_time[6:8] + ' ' + c_time[8:10] \
                          + ':' + c_time[10:12] + ':' + c_time[12:14]
        data['payFee'] = a.get('payFee')
        count_data.append(data)
    return count_data


def get_point():
    file_name = os.path.join(filedir, 'point.html')
    point = read_source(file_name)
    point = re.findall(""";">(.*?)</""", point)[0]
    print('count为：{}'.format(point))


def get_bill(task_id):
    file_name = os.path.join(filedir, str(task_id) + '\\' + 'bill.html')
    bill = read_source(file_name)
    bill = re.findall(""";">(.*?)</""", bill)[0]
    # print('bill：{}'.format(bill))
    bill_data = []
    bill = json.loads(str(bill))
    datas = bill.get('data')
    for a in datas:
        billMonth = a.get('billMonth')
        billFee = a.get('billFee')
        data = {}
        data['billMonth'] = billMonth
        data['billFee'] = billFee
        billMaterials = a.get('billMaterials')
        billMaterials1 = []
        for billMaterial in billMaterials:
            billMaterial.pop('remark')
            billMaterialInfos = billMaterial.get('billMaterialInfos')
            if billMaterialInfos:
                for billMaterialInfo in billMaterialInfos:
                    billMaterialInfo.pop('remark')
                billMaterials1.append(billMaterial)
        data['billMaterial'] = billMaterials1
        bill_data.append(data)
    return bill_data


if __name__ == '__main__':
    pass
