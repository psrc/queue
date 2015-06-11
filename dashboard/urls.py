from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from controller import views

urlpatterns = patterns('',
    url(r'^$', include('controller.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'register/$', views.register, name='register'),
    url(r'login/$', views.user_login, name='login'),
    url(r'logout/$', views.user_logout, name='logout'),
    url(r'about/$', views.about, name='about'),
    url(r'soundcast/$', views.soundcast, name='soundcast'),
    url(r'run-sc/$', views.run_soundcast, name='run_soundcast'),
    url(r'4k/$', views.fourkay, name='fourkay'),
    url(r'monitor/$', views.monitor, name='monitor'),
)
