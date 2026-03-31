from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

from .create_app import create_app

__all__ = ["create_app", "db", "migrate"]