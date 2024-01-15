import hashlib
import logging
import random
from datetime import datetime, timedelta
from dps_mysql_ha_sdk.utils.log_utils import to_serializable

import pymysql


def check_data_source(new_username, new_password, use_username, use_password):
    use_md5 = calculate_md5(use_username + use_password)
    new_md5 = calculate_md5(new_username + new_password)
    return use_md5 != new_md5


def calculate_md5(data):
    md5 = hashlib.md5()
    md5.update(data.encode('utf-8'))
    return md5.hexdigest()


def calculate_initial_delay_6():
    now = datetime.now().time()
    target_time = datetime.strptime("06:00", "%H:%M").time()

    if now < target_time:
        # 如果当前时间在6:00之前，返回当前时间到6:00的时间差
        time_difference = datetime.combine(datetime.today(), target_time) - datetime.combine(datetime.today(), now)
        return time_difference.total_seconds() + random.randint(0, 16 * 60 * 60)
    else:
        # 如果当前时间在6:00之后，返回当前时间到明天6:00的时间差
        tomorrow_target_time = datetime.combine(datetime.today() + timedelta(days=1), target_time)
        time_difference = tomorrow_target_time - datetime.combine(datetime.today(), now)
        return time_difference.total_seconds() + random.randint(0, 16 * 60 * 60)


def calculate_initial_delay_22():
    now = datetime.now().time()
    target_time = datetime.strptime("22:00", "%H:%M").time()

    # 获取今天的日期
    current_date = datetime.today().date()

    # 获取今天的22:00时间
    today_target_datetime = datetime.combine(current_date, target_time)

    # 如果当前时间在22:00之前，返回当前时间到22:00的时间差
    if now < target_time:
        time_difference = today_target_datetime - datetime.combine(current_date, now)
        return time_difference.total_seconds() + random.randint(0, 8 * 60 * 60)
    else:
        # 如果当前时间在22:00之后，返回当前时间到明天22:00的时间差
        tomorrow_target_datetime = today_target_datetime + timedelta(days=1)
        time_difference = tomorrow_target_datetime - datetime.combine(current_date, now)
        return time_difference.total_seconds() + random.randint(0, 8 * 60 * 60)


def test_mysql_credentials(host, port, username, password):
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            connect_timeout=5  # 设置连接超时时间
        )
        return True  # 账号密码有效
        connection.close()
    except pymysql.MySQLError as e:
        logging.error(f"Invalid MySQL credentials. Error: {e}")
        logging.error(
            to_serializable("ERROR", "db_utils",
                            "The backup account password is abnormal, and the data source will not be switched!"))
        return False  # 账号密码无效
