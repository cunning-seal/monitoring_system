from django.conf.urls import include, url
from django.contrib import admin
from internal_apps_set.views import data_udpate_view
from abonents.views import update_view

admin.autodiscover()
urlpatterns = [
    # Examples:
    # url(r'^$', 'monitoring_system.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^abonents/', include('abonents.urls')),
    url(r'^apps/', include('internal_apps_set.urls')),
    url(r'^connection_metrics/', include('connection_metrics.urls')),
    url(r'^database_metrics/', include('database_metrics.urls')),
    url(r'^errors/', include('error_packages.urls')),
    url(r'^hardware_metrics/', include('hardware_metrics.urls')),
    url(r'^external_apps/$', include('external_app_set.urls')),
    url(r'^$', include('mainpage.urls')),
    url(r'^ajax$', view=data_udpate_view, name="data_update_view"),
    url(r'^ajax2$', view=update_view, name="update_view"),
    # url(r'^ajax3$', view=er_update_view, name="er_update_view"),

]
