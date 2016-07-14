from datetime import datetime
from functools import wraps
from flask import jsonify, Response
import json


class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return int((obj - datetime(1970, 1, 1)).total_seconds())
        else:
            return json.JSONEncoder.default(self, obj)


def serialized(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        r = f(*args, **kwargs)
        if isinstance(r, Response):
            # Make this decorator idempotent
            return r
        else:
            return jsonify(r)
    return decorator
