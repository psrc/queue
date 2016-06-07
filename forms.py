import Pyro4
from wtforms import ValidationError


def verify_node_is_free(node):
    n = Pyro4.Proxy('PYRONAME:' + node)

    try:
        busy = n.is_busy()

    except:
        raise ValidationError('Node not responding.')

    if busy:
        raise ValidationError('Node is busy.')

    return True
