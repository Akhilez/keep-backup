from django.conf.urls import url

from keep import views

__author__ = 'Akhil'

urlpatterns = [
    url(r'^$', views.home, name="home"),
]
