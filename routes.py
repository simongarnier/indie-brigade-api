from blueprint import user, dev
from flask import Flask

app = Flask(__name__)
app.register_blueprint(user.user, url_prefix='/users')
app.register_blueprint(dev.dev, url_prefix='/users/<int:user_id>/devs')


if __name__ == "__main__":
    app.run(debug=True)
