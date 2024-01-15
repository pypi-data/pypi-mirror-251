import os
import time
from datetime import datetime


def date_format(timestamp):
    date_obj = datetime.fromtimestamp(timestamp / 1000.0)
    return date_obj.strftime("%Y-%m-%d %H:%M:%S")


def to_serializable(level, logger, msg):
    logstash_event = {
        "app_name": get_env_or_property("APPNAME"),
        "level": level,
        "log_time": date_format(time.time() * 1000),
        "logger": logger,
        "msg": msg
    }

    return map_to_json_string(logstash_event)


def get_env_or_property(key):
    return os.environ.get(key) or os.getenv(key) or None


def map_to_json_string(input_map):
    json_string = "{"
    first = True

    for key, value in input_map.items():
        if not first:
            json_string += ","
        json_string += f'"{key}":'

        if isinstance(value, str):
            json_string += f'"{value}"'
        else:
            json_string += str(value)

        first = False

    json_string += "}"
    return json_string
