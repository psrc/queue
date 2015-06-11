from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from controller import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'about/$', views.about, name='about'),
    url(r'launcher/$', views.launcher, name='launcher'),
    url(r'login/$', views.user_login, name='login'),
    url(r'logout/$', views.user_logout, name='logout'),
    url(r'monitor/$', views.monitor, name='monitor'),
    url(r'register/$', views.register, name='register'),
    url(r'run-sc/$', views.run_soundcast, name='run_soundcast'),
    url(r'soundcast/$', views.soundcast, name='soundcast'),
    url(r'4k/$', views.fourkay, name='fourkay'),
)
