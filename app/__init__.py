from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import os


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI_DEBUG1')

# debugsession would need to be changed to actual database connection
debugsession = Session(create_engine(TestConfig.SQLALCHEMY_DATABASE_URI))

db = SQLAlchemy()
migrate = Migrate()

# flask --app app --debug run
def create_app(config_class = Config):
    main_app = Flask(__name__)
    main_app.config.from_object(config_class)

    # flask --app app db init/migrate/upgrade
    db.init_app(main_app)
    migrate.init_app(main_app, db)

    with main_app.app_context():
        from app.dashapp.app import add_app
        main_app = add_app(main_app)

    return main_app

from app import models