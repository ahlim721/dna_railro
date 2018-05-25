"""railro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('home.urls')),
    url(r'^login/', include('home.urls')),
    url(r'^join/', include('home.urls')),
    url(r'^index/', include('home.urls')),
    url(r'^location/', include('location.urls')),
    url(r'^community/', include('community.urls')),
    url(r'^schedule/', include('schedule.urls')),
    url(r'^user_update/', include('mypage.urls')),

] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
