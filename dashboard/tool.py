import Pyro4
import logging, socket
from datetime import datetime

from .pluginmount import PluginMount
from .models import RunLog, Tool


class Tool:
    # TODO: update plugin docs
    """
    Mount point for plugins which refer to tools that can be run.

    Tools implementing this should provide the following attributes:
    =============  ========================================================
    title          Tool name - this will be visible in the URL bar

    view           The launcher form

    dbtable        The model holding run logs

    launcher_view  view method
    =============  ========================================================
    """

    # metaclass adds the 'plugins' attribute
    __metaclass__ = PluginMount
