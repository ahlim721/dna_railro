from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.community, name='community'),

    url(r'^show_write_form', views.show_write_form, name="show_write_form"),
    url(r'^DoWriteBoard', views.DoWriteBoard),
    url(r'^viewWork', views.viewWork),
    url(r'^viewForUpdate', views.viewForUpdate),
    url(r'^updateBoard', views.updateBoard),
    url(r'^viewForDelete', views.viewForDelete),
    url(r'^searchWithSubject', views.searchWithSubject),

    url(r'^listSearchedSpecificPageWork', views.listSearchedSpecificPageWork),
    url(r'^addComment', views.addComment),

]
