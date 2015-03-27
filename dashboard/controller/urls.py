from django.conf.urls import patterns, url
from controller import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'register/$', views.register, name='register'),
	url(r'login/$', views.user_login, name='login'),
	url(r'logout/$', views.user_logout, name='logout'),
	url(r'about/$', views.about, name='about'),
	url(r'soundcast/$', views.soundcast, name='soundcast'),
    url(r'run/$', views.get_name, name='get_name'),
	)