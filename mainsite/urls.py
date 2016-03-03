from django.conf.urls import patterns, include, url
from django.contrib import admin

from dashboard.tool import Tool
from dashboard import views

# this initializes all plugins
# from dashboard.plugins import *

# explicitly call all plugins for now since there is a hang-up with git imports
from dashboard.plugins import Demo, SoundCast

admin.autodiscover()


# Add URLs for each plugin
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'about/$', views.about, name='about'),
    url(r'launcher/$', views.launcher, name='launcher'),
    url(r'login/$', views.user_login, name='login'),
    url(r'logout/$', views.user_logout, name='logout'),
    url(r'monitor/$', views.monitor, name='monitor'),
    url(r'nodes/$', views.nodes, name='nodes'),
    url(r'nodes/(?P<server_id>[A-Za-z0-9_]+)/$', views.nodestatus, name='nodestatus'),
    url(r'register/$', views.register, name='register'),
    url(r'runlog/(?P<run_id>[0-9]+)/$', views.runlog, name='runlog'),
]

for tool in Tool.plugins:
    # this URL is for the launcher
    main_url = tool.title + r'/$'           # ex: 'soundcast/$'
    view = tool().view

    # todo this URL is for running the tool -- is this still needed?
    # run_title = 'run_' + title         # ex: 'run_soundcast'
    # run_url = 'run-' + title + r'/$'   # ex: 'run-soundcast/$'
    # run_view = tool.run_view

    # Add URL for the tool name
    urlpatterns.append(url(main_url, view, name=tool.title))

    # And add the tool name itself as a function definition in dashboard.views, pointing to the view
    setattr(views, tool.title, tool.view)
