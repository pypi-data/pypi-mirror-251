# -*- coding: utf-8 -*-
from datetime import datetime

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

    def execute(self, sql, params=None):
        """
        执行，返回的为 list，可单条也可多条
        """
        conn = self.pool.connection()
        cursor = conn.cursor()
        self.cursor = cursor

        try:
            if params is None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, params)
            return [self.__dict_datetime_obj_to_str(row_dict) for row_dict in cursor.fetchall()]
        except Exception as e:
            print(f"Cannot execute query all: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def __dict_datetime_obj_to_str(result_dict):
        """把字典里面的datetime对象转成字符串"""
        if result_dict:
            result_replace = {k: v.__str__() for k, v in result_dict.items() if isinstance(v, datetime)}
            result_dict.update(result_replace)
        return result_dict