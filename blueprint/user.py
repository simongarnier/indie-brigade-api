from flask import Blueprint
from utils import serialization, db

user = Blueprint('user', __name__)


@user.route('')
@serialization.serialized
def index():
    with db.get_ib_cursor() as cur:
        cur.execute("""
            SELECT id, email, firstname, lastname
            FROM users;
        """)
        return cur.fetchall()


@user.route('/<int:user_id>')
@serialization.serialized
def show(user_id):
    with db.get_ib_cursor() as cur:
        cur.execute("""
            SELECT *
            FROM users
            WHERE id = %s;
        """, [user_id])
        return cur.fetchone()
