import Pyro4
from Pyro4.errors import PyroError
from flask_wtf import Form
from wtforms import ValidationError, BooleanField
from wtforms import validators, StringField, FileField, SelectField, SubmitField, PasswordField


# VALIDATORS ---------------------------------
from wtforms.validators import DataRequired


def verify_node_is_free(form, field):
    node = field.data

    try:
        n = Pyro4.Proxy('PYRONAME:' + node)
        busy = n.is_busy()

    except PyroError:
        raise ValidationError('Network (Pyro) problem.')
    except:
        raise ValidationError('Node not responding.')

    if busy:
        raise ValidationError('Node is busy.')

    return True


def is_valid_file(f):
    """
    Test max size of 100k bytes
    """
    MAX_SIZE = 100000

    if f.size > MAX_SIZE:
        raise ValidationError('Too big: ' + f.name +
                              ' is larger than ' + str(MAX_SIZE) + ' bytes')
    return True


# FORMS ---------------------------------

class UserForm(Form):
    nickname = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
