from blueprint.user import user
from blueprint.dev import dev
from blueprint.skill import skill

from flask import Flask
from utils import db

app = Flask(__name__)

# User
app.register_blueprint(user, url_prefix='/users')

# Dev
app.register_blueprint(dev, url_prefix='/users/<int:user_id>/dev')
app.register_blueprint(dev, url_prefix='/devs')

# Skill
app.register_blueprint(skill, url_prefix='/skills')

@app.teardown_appcontext
def teardown(e):
    db.get_ib_conn().close()

if __name__ == "__main__":
    app.run(debug=True)
