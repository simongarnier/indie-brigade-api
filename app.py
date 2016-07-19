from flask import Flask, jsonify

from flask_cors import CORS

from blueprints.user import user
from blueprints.dev import dev
from blueprints.skill import skill
from blueprints.role import role

from utils import db, serialization

app = Flask(__name__)
app.json_encoder = serialization.DatetimeEncoder
app.url_map.strict_slashes = False
CORS(app, resources={r"/": {'origin': '*'}})


def register_on_dev_prefix(blueprint):
    app.register_blueprint(blueprint, url_prefix='/devs/<int:dev_id>/')
    app.register_blueprint(blueprint, url_prefix='/users/<int:user_id>/dev/')

# User
app.register_blueprint(user, url_prefix='/users/')

# Dev
app.register_blueprint(dev, url_prefix='/users/<int:user_id>/dev/')
app.register_blueprint(dev, url_prefix='/devs/')

# Skill
app.register_blueprint(skill, url_prefix='/skills/')
app.register_blueprint(skill, url_prefix='/roles/<int:role_id>/skills/')
register_on_dev_prefix(skill)

# Role
app.register_blueprint(role, url_prefix='/roles/')
register_on_dev_prefix(role)


# Errors
@app.errorhandler(404)
def not_found(e):
    return jsonify(status=e.name, message=e.description), 404


@app.teardown_appcontext
def teardown(e):
    db.get_ib_conn().close()

if __name__ == "__main__":
    app.run()
