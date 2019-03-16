#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2019/3/16
@Author  : wangjh
@desc    : PyCharm
"""
import os
import sys

cur_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(cur_dir))
import json
from flask import Flask, jsonify, request
from get_source.user_login_info import get_info, data_to_redis
from spider import start_spider
from parse_html.get_all_data import last_data
from base.handle_mongo import save_data_in_mongo
from mylog import log

app = Flask(__name__)


@app.route('/phone', methods=['POST'])
def index():
    phone_num = request.form.get('phone_num')
    serverpwd = request.form.get('serverpwd')
    task_id = request.form.get('task_id')
    os.makedirs('D:\work_space\ChinaMobile\html_source\{}'.format(str(task_id)))
    data = {
        'task_id': task_id,
        'phone_num': phone_num,
        'serverpwd': serverpwd,
        'smspwd': '',
        'status_code': 1
    }
    data_to_redis(task_id, data)

    start_spider(phone_num, task_id)
    # data = get_info(task_id)
    # data['status_code'] = #'页面获取完成,开始解析页面'
    # data_to_redis(task_id, data)
    log.crawler.info('页面获取完成,开始解析页面')

    all_data = last_data(task_id, phone_num)
    data = get_info(task_id)
    data['status_code'] = 3001
    data_to_redis(task_id, data)
    d = {
        'taskid': task_id,
        'result': all_data
    }
    save_data_in_mongo(d, "chinamobile")
    return jsonify(all_data)


@app.route('/sms', methods=['POST'])
def get_sms():
    smspwd = request.form.get('smspwd')
    task_id = request.form.get('task_id')
    data = get_info(task_id)
    data['smspwd'] = smspwd
    data['status_code'] = 2004
    data_to_redis(task_id, data)
    return '短信验证码保存成功'


if __name__ == '__main__':
    # app.config['JSON_AS_ASCII'] = False
    # app.run(host='0.0.0.0', port=8888)
    task_id = '3bc002b6cf8897652e1751c72008472d'
    phone_num = ''
    all_data = last_data(task_id, phone_num)
    data = json.dumps(all_data, ensure_ascii=True)
    print(data)
