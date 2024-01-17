# -*- coding: utf-8 -*-
import pymysql
from pymysql import OperationalError

from dps_mysql_ha_sdk.dynamic_pooled_db import DynamicPooledDB


class MySQLClient:
    def __init__(self,  platUrlMain, platUrl, platDsnKey, svcCode,
                 charset='utf8mb4'):
        try:
            self.pool = DynamicPooledDB(
                creator=pymysql,
                mincached=2,
                maxcached=10,
                maxconnections=10,
                charset=charset,
                autocommit=False,
                platUrlMain=platUrlMain,
                platUrl=platUrl,
                platDsnKey=platDsnKey,
                svcCode=svcCode,
                cursorclass=pymysql.cursors.DictCursor
            )
        except OperationalError as e:
            print(f"Cannot connect to database: {e}")
            exit(1)
