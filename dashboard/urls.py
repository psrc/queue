from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'register/$', views.register, name='register'),
    url(r'login/$', views.user_login, name='login'),
    url(r'logout/$', views.user_logout, name='logout'),
    url(r'about/$', views.about, name='about'),
    url(r'soundcast/$', views.soundcast, name='soundcast'),
    url(r'run-sc/$', views.run_soundcast, name='run_soundcast'),
    url(r'4k/$', views.fourkay, name='fourkay'),
    url(r'monitor/$', views.monitor, name='monitor'),
    ]
