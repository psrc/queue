from sqlalchemy.ext.hybrid import hybrid_property

from server import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    runs = db.relationship('RunLog', backref='user', lazy='dynamic')

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __unicode__(self): return self.username
    def __repr__(self): return '<User %r>' % self.username


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    project_contact = db.Column(db.String(255))
    modeling_contact = db.Column(db.String(255))

    def __unicode__(self): return self.name
    def __repr__(self): return '<Project %r>' % self.name


class RunLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    project = db.Column(db.String(128))
#    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    series = db.Column(db.String(3))
    note = db.Column(db.String(2048))
    status = db.Column(db.Integer)
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    tool = db.Column(db.String)
    tool_tag = db.Column(db.String(64))
    inputs = db.Column(db.String(2048))

    @hybrid_property
    def duration(self):
        try:
            length = str(self.end - self.start)
            length = length[:length.rfind('.')]
        except:
            length = ""

        return length

    def __repr__(self): return '<Runlog %s>' % str(self.id)
    def __unicode__(self):
        if self.project:
            return '%s - %s' % (self.project, self.series)
        else:
            return 'Run %s - %s' % (str(self.id), str(self.user))


