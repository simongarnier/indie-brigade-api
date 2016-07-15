from nestable_blueprint import  NestableBlueprint
from utils import serialization, db

role = NestableBlueprint('role', __name__, parent_keys=['user_id', 'dev_id'])

