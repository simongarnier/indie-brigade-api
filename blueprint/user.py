import json

from blueprint import db
from flask import Blueprint
from utils import encoding

user = Blueprint('user', __name__)

@user.route('/')
def index():
    cur = db.dict_cursor()
    cur.execute("""
        SELECT id, email, firstname, lastname
        FROM users;
    """)
    return json.dumps(cur.fetchall(), cls= encoding.DatetimeEncoder)

@user.route('/<int:user_id>/')
def show(user_id):
    cur = db.dict_cursor()
    cur.execute("""
        SELECT *
        FROM users
        WHERE id = %s;
    """, [user_id])
    return json.dumps(cur.fetchall(), cls= encoding.DatetimeEncoder)

