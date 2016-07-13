from blueprint import user, dev
from flask import Flask
from utils import db

app = Flask(__name__)

# User
app.register_blueprint(user.user, url_prefix='/users')

# Dev
app.register_blueprint(dev.dev, url_prefix='/users/<int:user_id>/dev')
app.register_blueprint(dev.dev, url_prefix='/devs')



@app.teardown_appcontext
def teardown(e):
    db.get_ib_conn().close()

if __name__ == "__main__":
    app.run(debug=True)
