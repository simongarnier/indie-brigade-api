from nestable_blueprint import NestableBlueprint
from flask import g
from utils import serialization, db, status

dev = NestableBlueprint('dev', __name__, parent_entity_key="user_id")


@dev.route('')
def index():
    cur = db.get_ib_cursor()
    if dev.context_id() is None:
        cur.execute("""
            SELECT id, description
            FROM devs;
        """)
    else:
        cur.execute("""
            SELECT *
            FROM devs
            WHERE user_id = %s;
        """, [dev.context_id()])
    return status.call_or_not_found(cur.fetchone(), serialization.sql_dict_as_json)


@dev.route('/<int:dev_id>')
def show(dev_id):
    cur = db.get_ib_cursor()
    if dev.context_id():
        cur.execute("""
            SELECT *
            FROM devs
            WHERE user_id = %s AND id = %s
        """, [dev.context_id(), dev_id])
    else:
        cur.execute("""
            SELECT *
            FROM devs
            WHERE id = %s
        """, [dev_id])
    return status.call_or_not_found(cur.fetchone(), serialization.sql_dict_as_json)

