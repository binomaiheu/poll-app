import os

"""
Required environment variables
1. select developmen or production config class : 

export POLL_CONFIG_SETUP=config.DevelopmentConfig
export POLL_CONFIG_SETUP=config.ProductionConfig
"""


class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SECRET_KEY = os.environ.get('SECRET_KEY')





