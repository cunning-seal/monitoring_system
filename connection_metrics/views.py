from django.shortcuts import render
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, Http404
from connection_metrics.models import AbonentConnectionMetric
from internal_apps_set.models import InternalApp
from external_app_set.models import ExternalApp
from datetime import datetime

class ForTemplate():
    def __init__(self, app_id, ext_app_name,recvB, sentB,conN, timeCon):
        self.app_id = app_id
        self.ext_app_name = ext_app_name
        self.receivedBytes = recvB
        self.sentBytes = sentB
        self.connectionNumber = conN
        self.timeCon = timeCon
        # self.last_con_metric = lConM

# def main_view(request):
#     try:
#
#         # metric_list = AbonentConnectionMetric.objects.order_by('app_id')
#         apps_set = InternalApp.objects.all()
#         info_list = []
#         for app in apps_set:
#             metric_set = AbonentConnectionMetric.objects.filter(app_id=app.id)
#             if len(metric_set) == 0:
#                 continue
#             summRecv = 0
#             summSent = 0
#             summConnNumber = 0
#             for ab in metric_set:
#                 summRecv += ab.receivedBytes
#                 summSent += ab.sentBytes
#                 summConnNumber += ab.connections_number
#
#             last_app_connection = AbonentConnectionMetric.objects.order_by('-timeCon').filter(app__id=app.id)[0]
#             info_list.append(ForTemplate(app.id, app.name, summRecv, summSent, summConnNumber, last_app_connection))
#
#     except AbonentConnectionMetric.DoesNotExist:
#         raise Http404("No such records!")
#
#     t = get_template('connection_metrics/index.html')
#     html = t.render(Context({'metric_list':info_list}))
#
#     return HttpResponse(html)

def main_view(request):

    data = []
    app_list = []
    apps_set = InternalApp.objects.all()
    ext_apps = ExternalApp.objects.all()
    for app in apps_set:
        metrics = AbonentConnectionMetric.objects.filter(app__id = app.id).order_by('-sendTime')
        # app_metrics = []
        for ext_app in ext_apps:
            last_ext_metric = metrics.filter(abonent=ext_app)
            if len(last_ext_metric) != 0:

                data.append(ForTemplate(app.id, ext_app.name,
                                               last_ext_metric[0].receivedBytes,
                                               last_ext_metric[0].sentBytes,
                                               last_ext_metric[0].connections_number,
                                               last_ext_metric[0].timeCon))
    t = get_template('connection_metrics/index2.html')
    html = t.render(Context({'metric_list':data, 'apps_list': apps_set}))
    return HttpResponse(html)
