__author__ = 'liuhui'


from django.conf.urls import url, include

from users import views

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^reset_password/$', views.reset_password, name='reset-password'),
]