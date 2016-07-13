from flask import Blueprint, g
from utils import serialization, db, status

dev = Blueprint('dev', __name__)


@dev.url_value_preprocessor
def get_dev_user(_, values):
    g.user_id = values.get('user_id', None)
    if g.user_id:
        values.pop('user_id')


@dev.route('')
def index():
    cur = db.get_ib_cursor()
    if g.user_id is None:
        cur.execute("""
            SELECT id, description
            FROM devs;
        """)
    else:
        cur.execute("""
            SELECT *
            FROM devs
            WHERE user_id = %s;
        """, [g.user_id])
    return status.call_or_not_found(cur.fetchone(), serialization.sql_dict_as_json)


@dev.route('/<int:dev_id>')
def show(dev_id):
    cur = db.get_ib_cursor()
    if g.user_id:
        cur.execute("""
            SELECT *
            FROM devs
            WHERE user_id = %s AND id = %s
        """, [g.user_id, dev_id])
    else:
        cur.execute("""
            SELECT *
            FROM devs
            WHERE id = %s
        """, [dev_id])
    return status.call_or_not_found(cur.fetchone(), serialization.sql_dict_as_json)

