# -*- coding: utf-8 -*-
__author__ = 'vivian'

import unittest

from db.db_utils import get_db_properties


class TestDBUtils(unittest.TestCase):
    def test_get_db_properties(self):
        url = "https://P901050302.dzqd.lio:9019/dss/db"
        plat_key = "0a0976679f3840bf9e64559f3e7d0c6e"
        svc_code = "P901011801"
        profile = "rc1"
        user_agent = svc_code
        databases = get_db_properties(url, plat_key, svc_code, profile, user_agent)
        for (k, v) in databases.items():
            print("dsn-n:%s, ip:%s, port:%d, sid:%s, username:%s, password:%s" %
                  (k, v["ip"], v["port"], v["sid"], v["username"], v["password"]))
{'ip': '172.16.50.127', 'password': 'XGEnjzF9_GJDqralcy', 'port': 3306, 'sid': 'dual_db', 'username': 'dual_user1'}