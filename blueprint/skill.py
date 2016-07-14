from nestable_blueprint import NestableBlueprint
from utils import serialization, db
from flask import request

skill = NestableBlueprint('skill', __name__, parent_keys=['user_id', 'dev_id', 'role_id'])


@skill.route('')
@serialization.serialized
def index():
    with db.get_ib_cursor() as cur:
        role_id = skill.parent_ids['role_id']
        if role_id:
            cur.execute("""
                SELECT *
                FROM skills
                WHERE role_id = %s;
            """, [role_id])
        else:
            cur.execute("""
                SELECT *
                FROM skills;
            """)
        return cur.fetchall()


@skill.route('/<int:skill_id>')
@serialization.serialized
def show(skill_id):
    return skill_for_id(skill_id)


@skill.route('major_skills')
@skill.route('minor_skills')
@serialization.serialized
def per_dev_index():
    if 'major_skills' in request.url_rule.rule:
        join_table = 'dev_major_skills'
    else:
        join_table = 'dev_minor_skills'
    dev_id = skill.parent_ids['dev_id']
    user_id = skill.parent_ids['user_id']
    return skills_for_dev(join_table, dev_id, user_id)


def skill_for_id(skill_id):
    with db.get_ib_cursor() as cur:
        cur.execute("""
            SELECT *
            FROM skills
            where id = %s
        """, [skill_id])
        return cur.fetchone()


def skills_for_dev(join_table, dev_id=None, user_id=None):
    with db.get_ib_cursor() as cur:
        if dev_id:
            cur.execute("""
                SELECT skills.*
                FROM skills
                JOIN {0} ON skills.id = {0}.skill_id
                WHERE {0}.dev_id = %s;
            """.format(join_table), [dev_id])
        elif user_id:
            cur.execute("""
                SELECT skills.*
                FROM skills
                JOIN {0} ON skills.id = {0}.skill_id
                JOIN devs ON devs.id = {0}.dev_id
                WHERE devs.user_id = %s;
            """.format(join_table), [user_id])
        return cur.fetchall()
