#!flask/bin/python
"""
Blockchain API
Api for connecting blockchain technology with a mobile application.
Blockchain: TRON;

Copyright (c) 2020 IDET.kz
Written by Galymzhan Abdymanap.
Version 1.0
"""

import logging
import traceback

from flask_restplus import Api
from rest_api import settings

# Create logger
log = logging.getLogger(__name__)

# Api init
api = Api(version='1.0', title='Tron Blockchain API',
          description='A simple demonstration of a Flask RestPlus powered API')


@api.errorhandler
def default_error_handler(e):
    """"""
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not settings.FLASK_DEBUG:
        return {'message': message}, 500



