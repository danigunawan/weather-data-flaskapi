"""
@author:     Fyzel@users.noreply.github.com

@copyright:  2017 Englesh.org. All rights reserved.

@license:    https://github.com/Fyzel/weather-data-flaskapi/blob/master/LICENSE

@contact:    Fyzel@users.noreply.github.com
@deffield    updated: 2017-06-14
"""

from os import path

import logging.config

from flask import Flask, Blueprint
from api.restplus import api
from flask_jwt import JWT, jwt_required, current_identity

import settings
from api.weather_data_api.business.security import authenticate, identity
from api.weather_data_api.endpoints.protected_humidity_data_endpoint import ns as protected_humidity_namespace
from api.weather_data_api.endpoints.protected_pressure_data_endpoint import ns as protected_pressure_namespace
from api.weather_data_api.endpoints.protected_temperature_data_endpoint import ns as protected_temperature_namespace
from api.weather_data_api.endpoints.public_humidity_data_endpoint import ns as public_humidity_namespace
from api.weather_data_api.endpoints.public_pressure_data_endpoint import ns as public_pressure_namespace
from api.weather_data_api.endpoints.public_temperature_data_endpoint import ns as public_temperature_namespace
from database import db


def create_app():
    app = Flask(__name__)
    return app


def configure_app(flask_app):
    if settings.FLASK_MODE is 'DEV':
        flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP
    flask_app.secret_key = settings.FLASK_SECRET_KEY


def initialize_app(flask_app):
    configure_app(flask_app)
    blueprint = Blueprint('weather', __name__, url_prefix='/weather')
    api.init_app(blueprint)
    api.add_namespace(protected_humidity_namespace)
    api.add_namespace(public_humidity_namespace)
    api.add_namespace(protected_pressure_namespace)
    api.add_namespace(public_pressure_namespace)
    api.add_namespace(protected_temperature_namespace)
    api.add_namespace(public_temperature_namespace)
    flask_app.register_blueprint(blueprint)

    db.init_app(flask_app)


log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
logging.config.fileConfig(log_file_path)
log = logging.getLogger(__name__)

app = create_app()
initialize_app(app)

jwt = JWT(app, authenticate, identity)


@app.route('/')
def index():
    return 'Computer says, "Hello."'


@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity


def main():
    initialize_app(app)

    if settings.FLASK_MODE is 'DEV':
        log.info('>>>>> Starting development server at http://{host}/{context}/ <<<<<'.format(
            host=app.config['SERVER_NAME'],
            context='weather')
        )


if __name__ == "__main__":
    app.run(debug=settings.FLASK_DEBUG)