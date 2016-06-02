import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# ###########################################################################
# App config & initialization

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.root_path, 'queue.sqlite'),
    SECRET_KEY="\x1348\xe8\xfa\x08\x15\x05\xa2_E\xbb}/,x\xf4\x8e\xcb\x1euVl\xdf\xd3|\xe2\xc3\xc1M\xa3\xdf",
    USERNAME='admin',
    PASSWORD='admin'
))
app.config.from_envvar('QUEUE_SETTINGS', silent=True)

#############################################################################
# DB models

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


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


# for tool in Tool.plugins:
#     # this URL is for the launcher
#     main_url = tool.title + r'/$'           # ex: 'soundcast/$'
#     view = tool().view
#
#     # todo this URL is for running the tool -- is this still needed?
#     # run_title = 'run_' + title         # ex: 'run_soundcast'
#     # run_url = 'run-' + title + r'/$'   # ex: 'run-soundcast/$'
#     # run_view = tool.run_view
#
#     # Add URL for the tool name
#     urlpatterns.append(url(main_url, view, name=tool.title))
#
#     # And add the tool name itself as a function definition in dashboard.views, pointing to the view
#     setattr(views, tool.title, tool.view)


if __name__ == "__main__":
    app.run()
