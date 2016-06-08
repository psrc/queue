import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'server.sqlite')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'fake_key'
USERNAME = 'admin'
PASSWORD = 'admin'
