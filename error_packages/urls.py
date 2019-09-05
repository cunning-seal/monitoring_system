from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^ajax/$', views.main_upload_data, name='main_view'),
    url(r'^$', views.main_view, name='main_view'),
    url(r'^ajax/$', views.er_update_view, name='update_view'),
    # url(r'^graph$', views.graph_view, name='graph_view'),
    #url(r'^(?P<app_number>[0-9]+)/$', views.app_metric, name='app_metric_view'),
]

