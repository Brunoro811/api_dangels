from flask import Flask
from environs import Env

from app import routes
from app.configs import database, migrations, cors


env = Env()
env.read_env()


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = env("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JSON_SORT_KEYS"] = False

    cors.init_app(app)
    database.init_app(app)
    migrations.init_app(app)
    routes.init_app(app)

    return app