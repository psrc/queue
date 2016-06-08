from server import db


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

