#!flask/bin/python
"""
Blockchain API
Api for connecting blockchain technology with a mobile application.
Blockchain: TRON;

Copyright (c) 2020 IDET.kz
Written by Galymzhan Abdymanap.
Version 1.0
"""

# import library
import logging.config
import os
from flask import Flask, Blueprint
import sys
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity
)
from flask_mail import Mail

# import support modules from this project
from rest_api import settings
from rest_api.api.blockchain.endpoints.payable import ns as payable_namespace
from rest_api.api.blockchain.endpoints.free import ns as free_namespace
from rest_api.api.restplus import api


#------------------------------------------------------------------------------------
# Flask init
#------------------------------------------------------------------------------------

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'  # 

#------------------------------------------------------------------------------------
# Config MAIL-SERVER
#------------------------------------------------------------------------------------
app.config.update(dict(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'abdizhan09@gmail.com',
    MAIL_PASSWORD = 'abdizhan09',
))
mail = Mail(app)
#------------------------------------------------------------------------------------

# Web token init 
jwt = JWTManager(app)


# Create logger and config logger
logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logging.conf'))
logging.config.fileConfig(logging_conf_path)
# Configure logger, 
logging.basicConfig(level = log_level, filename = 'logs/logs.txt', format='%(asctime)s :: %(name)s - %(levelname)s :: %(message)s')
log = logging.getLogger(__name__)






def configure_app(flask_app):
    """App configuration"""
    #flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP


def initialize_app(flask_app):
    """App init"""
    configure_app(flask_app)
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(payable_namespace)
    api.add_namespace(free_namespace)
    flask_app.register_blueprint(blueprint)


def main():
    """Run app"""
    initialize_app(app)
    #log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))
    log.info('>>>>> Starting development server at http://172.16.3.75/api/ <<<<<')
    app.run(host='172.16.3.75', port='8837', debug=settings.FLASK_DEBUG)


if __name__ == "__main__":
    main()
