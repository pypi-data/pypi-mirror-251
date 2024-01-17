# -*- coding: utf-8 -*-
import os
import threading
import time

from dps_mysql_ha_sdk.mysql_client_tools import MySQLClient


# 初始化连接
connector = MySQLClient(
    # host='xx',
    # port=xx,
    # user='xx',
    # password='xx',
    # database='xx',
    platUrlMain="https://test.example1.com/dss/db",
    platUrl="https://test.example2.com/dss/db",
    platDsnKey="DSN-1",
    svcCode="xx",
)

connector1 = MySQLClient(
    # host='xx',
    # port=xx,
    # user='xx',
    # password='xx',
    # database='xx',
    platUrlMain="https://test.example1.com/dss/db",
    platUrl="https://test.example2.com/dss/db",
    platDsnKey="DSN-1",
    svcCode="xx",
)


def worker(connector,connector1):
    while True:
        # 查询数据
        username = connector.execute("SELECT USER()")
        username1 = connector1.execute("SELECT USER()")
        print(username)
        print(username1)
        # 添加一些延时，避免太快
        time.sleep(1)


# 创建多个线程来执行 worker 函数
threads = []
for _ in range(int(10)):
    thread = threading.Thread(target=worker, args=(connector,connector1))
    threads.append(thread)

# 启动线程
for thread in threads:
    thread.start()

# 主线程等待所有线程完成
for thread in threads:
    thread.join()
