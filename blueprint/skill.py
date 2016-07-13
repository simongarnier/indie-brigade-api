from nestable_blueprint import NestableBlueprint
from utils import serialization, db, status

skill = NestableBlueprint('skill', __name__, parent_entity_key="user_id")


@skill.route('')
def index():
    cur = db.get_ib_cursor()
    cur.exectute("""
        SELECT *
        FROM skills;
    """)
    return status.call_or_not_found(cur.fetchall(), serialization.sql_dict_as_json)


