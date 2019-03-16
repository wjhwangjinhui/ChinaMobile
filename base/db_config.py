#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2019/3/16
@Author  : wangjh
@desc    : PyCharm
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import redis
import platform

pl = platform.system()
if pl == "Linux":
    engine = create_engine('mysql+pymysql://root:123456@127.0.0.1:3306/test?charset=utf8mb4')
else:
    engine = create_engine('mysql+pymysql://root:123456@localhost:3306/test?charset=utf8mb4')
DBSession = sessionmaker(bind=engine)


class RedisPool:
    if pl == "Windows":
        def __init__(self, client_host="127.0.0.1", client_port=6379, client_db=0):
            self.client_host = client_host
            self.client_port = client_port
            self.client_db = client_db
    else:
        def __init__(self, client_host="127.0.0.1", client_port=6379, client_db=0):
            self.client_host = client_host
            self.client_port = client_port
            self.client_db = client_db

    def redis_pool(self):
        if pl == "Windows":
            pool = redis.ConnectionPool(
                host=self.client_host,
                port=self.client_port,
                db=self.client_db)
        else:
            pool = redis.ConnectionPool(
                host=self.client_host,
                port=self.client_port,
                db=self.client_db)
        return redis.StrictRedis(connection_pool=pool)


if __name__ == '__main__':
    pass

