from flask import Blueprint
from utils import serialization, db, status

user = Blueprint('user', __name__)

@user.route('')
def index():
    cur = db.get_ib_cursor()
    cur.execute("""
        SELECT id, email, firstname, lastname
        FROM users;
    """)
    return status.call_or_not_found(cur.fetchone(), serialization.sql_dict_as_json)


@user.route('/<int:user_id>')
def show(user_id):
    cur = db.get_ib_cursor()
    cur.execute("""
        SELECT *
        FROM users
        WHERE id = %s;
    """, [user_id])
    return status.call_or_not_found(cur.fetchone(), serialization.sql_dict_as_json)


