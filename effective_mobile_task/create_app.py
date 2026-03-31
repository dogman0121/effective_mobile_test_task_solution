from flask import Flask, jsonify

from .routes import bp
from . import db, migrate
from .containers import AppContainer
from .exceptions import ApiException

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    app.register_blueprint(bp)
    db.init_app(app)
    migrate.init_app(app, db)
    

    container = AppContainer()
    container.config.from_dict(app.config)
    container.db_session.override(db.session)

    app.container = container

    return app
