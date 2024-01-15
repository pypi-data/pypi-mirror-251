import os
import threading
import time
import logging

import requests
import yaml
from dbutils.pooled_db import PooledDB

from dps_mysql_ha_sdk.utils.check_utils import check_data_source, calculate_initial_delay_6, calculate_initial_delay_22, \
    test_mysql_credentials
from dps_mysql_ha_sdk.utils.log_utils import to_serializable


# class LogFactory:
#     @staticmethod
#     def getLog(clazz):
#         return logging.getLogger(clazz)


class CustomPooledDB(PooledDB):
    def __init__(self, *args, **kwargs):
        self.password = None
        self.user = None
        self.database = None
        self.port = None
        self.host = None
        self.svcCode = None
        self.platDsnKey = None
        self.platUrlMain = None
        self._mincached = kwargs['mincached']
        self.platUrlMain = kwargs['platUrlMain']
        self.platUrl = kwargs['platUrl']
        self.platDsnKey = kwargs['platDsnKey']
        self.svcCode = kwargs['svcCode']
        self.get_db_info(**kwargs)

        kwargs.pop('platUrlMain', None)
        kwargs.pop('platUrl', None)
        kwargs.pop('platDsnKey', None)
        kwargs.pop('svcCode', None)
        kwargs['host'] = self.host
        kwargs['port'] = self.port
        kwargs['database'] = self.database
        kwargs['user'] = self.user
        kwargs['password'] = self.password
        super().__init__(*args, **kwargs)
        # 开启定时检查任务
        check_thread = threading.Thread(target=self._init_check_task)
        check_thread.daemon = True  # 设置为守护线程，程序退出时自动退出
        check_thread.start()
        # 开启切换数据源任务
        update_thread = threading.Thread(target=self._init_update_task)
        update_thread.daemon = True  # 设置为守护线程，程序退出时自动退出
        update_thread.start()

    def get_db_info(self, **kwargs):
        if 'platUrlMain' in kwargs and kwargs['platUrlMain'] is not None:
            url = kwargs['platUrlMain']
        else:
            url = self.platUrl
        platkey = os.environ.get("PLATKEY", None)
        profile = os.environ.get("PROFILE", None)
        user_agent = self.svcCode
        databases = None
        logging.warning(
            to_serializable("WARNING", "dynamic_pooled_db",
                            "url:" + url + " platkey:" + platkey + " svcCode:" + self.svcCode
                            + " profile:" + profile + " user_agent:" + user_agent))
        try:
            # databases = get_db_properties(self.platUrlMain, platkey, self.svcCode, profile, user_agent)
            url = "http://127.0.0.1:8081/db/"
            response = requests.get(url)
            res_bytes = response.text
            data = yaml.load(res_bytes, Loader=yaml.FullLoader)
            databases = data["database"]
        except Exception as e:
            logging.error(f"Error while getting database properties: {e}")
            logging.error(
                to_serializable("ERROR", "dynamic_pooled_db",
                                "Exception in calling the data source platform to obtain MYSQL database parameters "
                                "interface! url:" + url))

        # 设置对象的属性
        if databases is not None:
            self.host = databases.get(self.platDsnKey).get("ip")
            self.port = databases.get(self.platDsnKey).get("port")
            self.database = databases.get(self.platDsnKey).get("sid")
            logging.warning(
                to_serializable("WARNING", "dynamic_pooled_db",
                                "host:" + self.host + " port:" + str(self.port) + " sid:" + self.database
                                + " username:" + databases.get(self.platDsnKey).get("username") + " password:"
                                + databases.get(self.platDsnKey).get("password")))
            if self.user is None or self.password is None:
                self.user = databases.get(self.platDsnKey).get("username")
                self.password = databases.get(self.platDsnKey).get("password")
            elif check_data_source(databases.get(self.platDsnKey).get("username"),
                                   databases.get(self.platDsnKey).get("password"),
                                   self.user, self.password):
                # 账号密码发生变化暂时将账号密码保存在内存中
                logging.warning(
                    to_serializable("WARNING", "dynamic_pooled_db",
                                    "自定义资源标签" + self.platDsnKey + " 账号密码已发生变化，暂时将账号密码保存在内存中! "
                                    + self.user + "->" + databases.get(self.platDsnKey).get("username")))
                self.user = databases.get(self.platDsnKey).get("username")
                self.password = databases.get(self.platDsnKey).get("password")
            else:
                logging.warning(
                    to_serializable("WARNING", "dynamic_pooled_db",
                                    "自定义资源标签" + self.platDsnKey + " 账号密码无变化! "))

    def connection(self, shareable=True):
        with self._lock:
            # 调用父类的 connection 方法
            con = super(CustomPooledDB, self).connection(shareable)
            if not hasattr(con, 'userName') or con.userName is None:
                con._con.userName = self._kwargs['user']
                return con
            else:
                if con._con.userName != self._kwargs['user']:
                    try:
                        con._con.close()
                        self._connections -= 1
                        if len(self._idle_cache) == 0:
                            # 创建新的连接保存到 _idle_cache 中
                            self._idle_cache.extend([self.dedicated_connection() for i in range(self._mincached)])
                        return self.connection()
                    except Exception:
                        pass
            return con

    def _init_check_task(self):
        # 启动定时任务
        initialDelay = calculate_initial_delay_6()
        time.sleep(int(os.environ.get("check.init")) if os.environ.get("check.init") else initialDelay)
        logging.warning(
            to_serializable("WARNING", "dynamic_pooled_db",
                            "Start checking account and password changes task in "
                            + os.environ.get("check.init") + " seconds" if os.environ.get("check.init") else str(
                                initialDelay) + " seconds"))
        self._start_check_task()

    def _start_check_task(self):
        # 创建一个 Timer 对象，指定定时任务的函数和间隔时间
        timer = threading.Timer(int(os.environ.get("check.period")) if os.environ.get("check.period") else 12 * 60 * 60,
                                self._check_task)
        # 设置为守护线程，程序退出时自动退出
        timer.daemon = True
        # 启动定时任务
        timer.start()

    def _check_task(self):
        # 定时任务逻辑
        self.get_db_info()
        # 重新启动下一个定时任务
        self._start_check_task()

    def _init_update_task(self):
        # 启动定时任务
        initialDelay = calculate_initial_delay_22()
        time.sleep(int(os.environ.get("update.init")) if os.environ.get("update.init") else initialDelay)
        logging.warning(
            to_serializable("WARNING", "dynamic_pooled_db",
                            "Start the update account and password task in "
                            + os.environ.get("update.init") + " seconds" if os.environ.get("update.init") else str(
                                initialDelay) + " seconds"))
        self._start_update_task()

    def _start_update_task(self):
        # 创建一个 Timer 对象，指定定时任务的函数和间隔时间
        timer = threading.Timer(
            int(os.environ.get("update.period")) if os.environ.get("update.period") else 24 * 60 * 60,
            self._update_task)
        # 设置为守护线程，程序退出时自动退出
        timer.daemon = True
        # 启动定时任务
        timer.start()

    def _update_task(self):
        logging.warning(
            to_serializable("WARNING", "dynamic_pooled_db",
                            "Custom resource label " + self.platDsnKey + " executes update data source task"))
        # 检查3次
        if test_mysql_credentials(self.host, self.port, self.user, self.password) \
                and test_mysql_credentials(self.host, self.port, self.user, self.password) \
                and test_mysql_credentials(self.host, self.port, self.user, self.password):
            self._kwargs["user"] = self.user
            self._kwargs["password"] = self.password
        # 重新启动下一个定时任务
        self._start_update_task()
