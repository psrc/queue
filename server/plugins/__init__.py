# This finds all folders in the plugin directory and adds them to _all_ so they get imported.
import os

# get folder name so we can search for plugin folders
FOLDER = __name__.replace('.','/')
__all__ = [name for name in os.listdir(FOLDER) if os.path.isdir(FOLDER+'/'+name)]

# This import 'magically' attaches all plugins to the ModelPlugin mount point
# See http://martyalchin.com/2008/jan/10/simple-plugin-framework/
from server.plugins import *
from server.pluginmount import ModelPlugin


def register_plugins(app):
    """Register Flask app URLs based on the found plugin folders"""
    for tool in ModelPlugin.get_plugins():
        print 'Found plugin: /' + tool.title
        main_url = '/' + tool.title + '/'  # ex: 'soundcast/$'
        view = tool.view

        app.add_url_rule(main_url, tool.title, view, methods=['GET','POST'])
