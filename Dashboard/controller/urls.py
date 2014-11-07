from django.conf.urls import patterns, url
from controller import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'))