from sqlalchemy.ext.hybrid import hybrid_property

from server import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    agency_id = db.Column(db.Integer, db.ForeignKey('agency.id'))
    runs = db.relationship('RunLog', backref='user', lazy='dynamic')

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __init__(self, nickname, email):
        self.nickname = nickname
        self.email = email

    def __unicode__(self):
        return self.nickname

    def __repr__(self):
        return '<User %r>' % self.nickname


class Agency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    members = db.relationship('User', backref='agency', lazy='dynamic')

    def __unicode__(self): return self.name

    def __repr__(self): return '<Agency %r>' % self.name


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
            length = ''

        return length

    def __repr__(self): return '<Runlog %s>' % str(self.id)
    def __unicode__(self):
        if self.project:
            return '%s - %s' % (self.project, self.series)
        else:
            return 'Run %s - %s' % (str(self.id), str(self.user))


