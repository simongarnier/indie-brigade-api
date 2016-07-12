import json

from blueprint import db
from flask import Blueprint
from utils import encoding

dev = Blueprint('dev', __name__)

@dev.route('/')
def index():
    cursor = db.dict_cursor()
    cursor.execute("""
        SELECT id, description
        FROM devs;
    """)
    return json.dumps(cursor.fetchone(), cls=encoding.DatetimeEncoder)
