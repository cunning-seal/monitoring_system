from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.main_view, name='main_view'),
    url(r'^(?P<abonent_id>[0-9]+)/$', views.abonent_view, name='abonent_view'),
    url(r'^(?P<abonent_id>[0-9]+)/error$', views.error_view, name='error_view'),
    url(r'^(?P<abonent_id>[0-9]+)/graph$', views.graph_view, name='graph_view'),
    url(r'^ajax/$', views.update_view, name='update_view'),

]