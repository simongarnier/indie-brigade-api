import json
from datetime import datetime


class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return int((obj - datetime(1970, 1, 1)).total_seconds())
        else:
            return json.JSONEncoder.default(self, obj)


def sql_dict_as_json(sql_dict):
    return json.dumps(sql_dict, cls=DatetimeEncoder)
