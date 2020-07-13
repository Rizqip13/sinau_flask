import os

from flask import Flask

from .extensions import db, ma 
from . import main 


def create_app():
    app=Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI']   = os.environ['DATABASE_URI']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # extensions
    db.init_app(app)
    ma.init_app(app)

    @app.before_first_request
    def create_tables():
        db.engine.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        db.create_all()

    app.register_blueprint(main.bp)

    return app 