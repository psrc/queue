import os
from config import basedir
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager
from flask_openid import OpenID

app = Flask(__name__)
app.config.from_object('config')

Bootstrap(app)

# Login manager and OpenID support
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))

# DB and migration support
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# imports are below app instantiation to avoid circular references
from server import views, models, forms
