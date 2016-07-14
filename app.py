from blueprint.user import user
from blueprint.dev import dev
from blueprint.skill import skill

from flask import Flask, jsonify
from utils import db, serialization

app = Flask(__name__)
app.json_encoder = serialization.DatetimeEncoder

# User
app.register_blueprint(user, url_prefix='/users')

# Dev
app.register_blueprint(dev, url_prefix='/users/<int:user_id>/dev')
app.register_blueprint(dev, url_prefix='/devs')

# Skill
app.register_blueprint(skill, url_prefix='/skills')
app.register_blueprint(skill, url_prefix='/roles/<int:role_id>/skills')
app.register_blueprint(skill, url_prefix='/devs/<int:dev_id>/')
app.register_blueprint(skill, url_prefix='/users/<int:user_id>/dev/')


# Errors
@app.errorhandler(404)
def not_found(e):
    return jsonify(status=e.name, message=e.description), 404


@app.teardown_appcontext
def teardown(e):
    db.get_ib_conn().close()

if __name__ == "__main__":
    app.run(debug=False)
