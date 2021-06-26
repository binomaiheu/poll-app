import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'poll.db' )
SECRET_KEY = 'ch3ckm3'
SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = True

