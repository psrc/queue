# This finds all folders in the plugin directory and adds them to _all_ so they get imported.
import os

# get folder name so we can search for plugin folders
FOLDER = __name__ + '/'
__all__ = [plugin for plugin in os.listdir(FOLDER) if os.path.isdir(FOLDER + plugin)]

# This import 'magically' attaches all plugins to the ModelPlugin mount point
# See http://martyalchin.com/2008/jan/10/simple-plugin-framework/
from plugins import *
from plugins.pluginmount import ModelPlugin


def register_plugins(app):
    """Register Flask app URLs based on the found plugin folders"""
    for tool in ModelPlugin.get_plugins():
        print 'Found plugin: /' + tool.title

        launcher_url = '/' + tool.title + '/'  # ex: 'soundcast/$'

        app.add_url_rule(launcher_url, tool.title, tool.launcher,
                         methods=['GET','POST'])
