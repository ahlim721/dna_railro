from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.signin, name='login'),
    url(r'^login/', views.signin, name='login'),
    url(r'^index/', views.home, name='home'),
    url(r'^join/', views.signup, name='join'),
]
