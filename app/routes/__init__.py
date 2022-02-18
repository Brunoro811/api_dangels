from flask import Flask

from app.routes.api.api_route import bp as bp_api


def init_app(app: Flask):
    app.register_blueprint(bp_api)
