from nestable_blueprint import NestableBlueprint
from utils import serialization, db
from flask import abort
import skill

dev = NestableBlueprint('dev', __name__, parent_keys=['user_id'])


@dev.route('', methods=['GET'])
@serialization.serialized
def index():
    user_id = dev.parent_ids['user_id']
    if user_id is None:
        with db.get_ib_cursor() as cur:
            cur.execute("""
                SELECT id, description
                FROM devs;
            """)
        return cur.fetchall()
    else:
        return show()


@dev.route('<int:dev_id>', methods=['GET'])
@serialization.serialized
def show(dev_id=None):
    with db.get_ib_cursor() as cur:
        user_id = dev.parent_ids['user_id']
        if user_id and dev_id:
            cur.execute("""
                SELECT *
                FROM devs
                WHERE user_id = %s AND id = %s
            """, [user_id, dev_id])
        elif dev_id:
            cur.execute("""
                SELECT *
                FROM devs
                WHERE id = %s
            """, [dev_id])
        elif user_id:
            cur.execute("""
                SELECT *
                FROM devs
                WHERE user_id = %s;
            """, [user_id])
        else:
            abort(404)
        fetched_dev = cur.fetchone()
        fetched_dev['minor_skills'] = skill.skills_for_dev('dev_minor_skills', dev_id=dev_id, user_id=user_id)
        fetched_dev['major_skills'] = skill.skills_for_dev('dev_major_skills', dev_id=dev_id, user_id=user_id)
        fetched_dev['main_skill'] = skill.skill_for_id(fetched_dev['main_skill_id'])
        return fetched_dev

