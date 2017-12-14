from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^new_user$', views.new_user),
    url(r'^login$', views.login),
    url(r'^main$', views.main),
    url(r'^dump_users$', views.dump_users),
    url(r'^logout$', views.logout)
]