from nestable_blueprint import  NestableBlueprint
from utils import serialization, db
from flask import abort

role = NestableBlueprint('role', __name__, parent_keys=['user_id', 'dev_id'])
detail_role_query = """
    SELECT roles.*
    FROM roles
    JOIN devs ON devs.role_id = roles.id
    WHERE {0} = %s;
"""


@role.route('', methods=['GET'])
@serialization.serialized
def index():
    with db.get_ib_cursor() as cur:
        cur.execute("""
            SELECT id, code
            FROM roles;
        """)
        return cur.fetchall()


@role.route('<int:role_id>', methods=['GET'])
@role.route('role', methods=['GET'])
@serialization.serialized
def show(role_id=None):
    user_id = role.parent_ids['user_id']
    dev_id = role.parent_ids['dev_id']
    if user_id:
        return role_for_user(user_id)
    elif dev_id:
        return role_for_dev(dev_id)
    elif role_id:
        with db.get_ib_cursor() as cur:
            cur.execute("""
                SELECT roles.*
                FROM roles
                WHERE id = %s;
            """, [role_id])
            return cur.fetchone()


def role_for_user(user_id):
    if user_id:
        with db.get_ib_cursor() as cur:
            cur.execute(detail_role_query.format('user_id'), [user_id])
            return cur.fetchone()
    else:
        abort(404)


def role_for_dev(dev_id):
    if dev_id:
        with db.get_ib_cursor() as cur:
            cur.execute(detail_role_query.format('devs.id'), [dev_id])
            return cur.fetchone()
    else:
        abort(404)
