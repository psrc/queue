import os, datetime
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'server.sqlite')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'fake_key'
USERNAME = 'admin'
PASSWORD = 'admin'
YEAR = datetime.datetime.now().year

WTF_CSRF_ENABLED = True

OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}
]

