# main file for server management
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .db_form import db, capstone_session, teams, students, team_members, reports

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='NotSoSecret',
    )

    return app
