"""possster URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import login
from django.contrib.auth.views import logout
from django.conf.urls.static import static
from django.conf import settings
from poster.views import PosterLV
from poster.views import PosterIndex
from poster.views import PosterCV
from possster.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', PosterIndex.as_view(), name='index'),
    url(r'^add/$', PosterCV.as_view(), name='add'),
    url(r'^poster/$', PosterLV.as_view(), name='poster'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^register/$', UserCV.as_view(), name='register'),
    url(r'^register/done$', UserCreateDoneTV.as_view(), name='register_done'),
    url(r'^mypage/$', UserTV.as_view(), name='mypage'),
    url(r'^register/remove/(?P<pk>\d+)/$', UserDV.as_view(), name='register_remove'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
