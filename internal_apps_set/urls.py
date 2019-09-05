from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.main_view, name='main_view'),
    url(r'^(?P<app_id>[0-9]+)/$', views.main_2, name='main_2'),

]