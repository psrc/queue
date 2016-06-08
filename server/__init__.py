from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

Bootstrap(app)
db = SQLAlchemy(app)

# imports are below app instantiation to avoid circular references
from server import views, models, forms, plugins
