#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2019/3/16
@Author  : wangjh
@desc    : PyCharm
"""
import pymongo

# 连接数据库
client = pymongo.MongoClient('127.0.0.1', 27017)
db = client['test']


def save_data_in_mongo(data, table):
    table = db[table]
    table.insert_one(data)
