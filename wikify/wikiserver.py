import importlib
from flask import Flask


class Setting:
    port: int
    database: str
    prefix: str
    register: bool

setting: Setting = Setting()

def create_app():
    app = Flask(__name__)
    from .middlewares import middlewares
    app.register_blueprint(middlewares)
    from .routes import routes
    app.register_blueprint(routes)
    importlib.import_module("wikify.autoload")
    return app

def run():
    app = create_app()
    app.run(host="0.0.0.0", port=setting.port, debug=True)
