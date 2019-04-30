# main file for server management --- Do we still need this?
from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='NotSoSecret',
    )

    return app
