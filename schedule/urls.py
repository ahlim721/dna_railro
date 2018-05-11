from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.schedule, name='schedule'),
    url(r'^test_api',views.test_api, name="test_api"),
    url(r'^create/(\d+)', views.create, name="create"),
    url(r'^doschedule', views.doschedule, name="doschedule"),
]
