import Pyro4
from Pyro4.errors import PyroError
from wtforms import ValidationError


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
