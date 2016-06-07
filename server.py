import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

# ###########################################################################
# App config & initialization
from wtforms import ValidationError

app = Flask(__name__)
Bootstrap(app)

app.config.from_object(__name__)
app.config.update(dict(
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.root_path, 'queue.sqlite'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SECRET_KEY="fake_key",
    USERNAME='admin',
    PASSWORD='admin'
))
app.config.from_envvar('QUEUE_SETTINGS', silent=True)

db = SQLAlchemy(app)

#############################################################################
# DB models


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    project_contact = db.Column(db.String(256))
    modeling_contact = db.Column(db.String(256))

    def __unicode__(self): return self.name
    class Meta: ordering = ['name']


class Tool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    url = db.Column(db.String(1024))
    def __unicode__(self): return self.name
    class Meta: ordering = ['name']


class RunLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    series = db.Column(db.String(3))
    note = db.Column(db.String(2048))
    status = db.Column(db.Integer)
    start = db.Column(db.DateTime)
    duration = db.Column(db.DateTime)
    tool = db.Column(db.String)
    tool_tag = db.Column(db.String(64))
    inputs = db.Column(db.String(2048))

    def __unicode__(self):
        if (self.project):
            return '' + self.project + ' - ' + self.series
        else:
            return 'Run ' + str(self.id) + ' - ' + str(self.user)

    class Meta: ordering = ['-start']


#############################################################################
# App entry points

@app.route("/")
def view_index():
    return render_template('index.html', user=None)


@app.route('/about/')
def view_about():
    return render_template('about.html', user=None)


@app.route('/launcher/')
def view_launcher():
    return render_template('launcher.html', user=None)


@app.route('/login/')
@app.route('/logout/')
@app.route('/monitor/')
@app.route('/nodes/')
@app.route('/nodes/<server_id>')
@app.route('/register/')
@app.route('/runlog/<int:run_id>/')
def xmeow():
    return "<i><b>COMING SOON!</b></i>"

#############################################################################
# App entry points for plug-ins

from pluginmount import ModelPlugin

# This import 'magically' attaches all plugins to the ModelPlugin mount point
# See http://martyalchin.com/2008/jan/10/simple-plugin-framework/
from plugins import *

for tool in ModelPlugin.get_plugins():
    print tool.title
    main_url = '/' + tool.title + '/'  # ex: 'soundcast/$'
    view = tool.view

    app.add_url_rule(main_url, tool.title, view)

    # todo And add the tool name itself as a function definition in dashboard.views,
    # pointing to the view
    # setattr(views, tool.title, tool.view)

if __name__ == "__main__":
    print app.url_map
    app.run()
