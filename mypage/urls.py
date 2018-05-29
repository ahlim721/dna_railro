from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.user_leave, name='user_leave'),
    url(r'^user_leave', views.user_leave, name='user_leave'),
    url(r'^user_travellist', views.user_travellist, name='user_travellist')
]
