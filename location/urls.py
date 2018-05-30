from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.location, name='location'),
    url(r'^searchLoc', views.searchLoc, name='searchLoc'),
]
