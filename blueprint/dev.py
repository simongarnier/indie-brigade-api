from nestable_blueprint import NestableBlueprint
from utils import serialization, db, status

dev = NestableBlueprint('dev', __name__, parent_keys=['user_id'])


@dev.route('')
def index():
    cur = db.get_ib_cursor()
    user_id = dev.parent_ids['user_id']
    if user_id is None:
        cur.execute("""
            SELECT id, description
            FROM devs;
        """)
    else:
        cur.execute("""
            SELECT *
            FROM devs
            WHERE user_id = %s;
        """, [user_id])
    return status.call_or_not_found(cur.fetchone(), serialization.sql_dict_as_json)


@dev.route('/<int:dev_id>')
def show(dev_id):
    cur = db.get_ib_cursor()
    user_id = dev.parent_ids['user_id']
    if user_id:
        cur.execute("""
            SELECT *
            FROM devs
            WHERE user_id = %s AND id = %s
        """, [user_id, dev_id])
    else:
        cur.execute("""
            SELECT *
            FROM devs
            WHERE id = %s
        """, [dev_id])
    return status.call_or_not_found(cur.fetchone(), serialization.sql_dict_as_json)

