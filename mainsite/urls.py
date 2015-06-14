from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from dashboard import views

urlpatterns = patterns('',
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
    url(r'soundcast/$', views.soundcast, name='soundcast'),
    url(r'4k/$', views.fourkay, name='fourkay'),
)
