from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from django.template.loader import get_template
from django.template import Context
from internal_apps_set.models import InternalApp
from external_app_set.models import ExternalApp
from connection_metrics.models import AbonentConnectionMetric
from datetime import datetime, time
import time as tt
import pytz

def main_view(request):
    apps_list = InternalApp.objects.all()
    if len(apps_list) == 0:
        raise Http404("LEN = " + str(len(apps_list)))
    t = get_template('internal_apps_set/index.html')
    html = t.render(Context({'apps_list': apps_list}))
    return HttpResponse(html)

class Res():
    def __init__(self, ab, sB, rB, conT,disconT,r_conT,r_disconT, flag, conN):
        self.abonent = ab
        self.sentB = sB
        self.recvB = rB
        self.conT = conT
        self.disconT = disconT
        self.r_conT = r_conT
        self.r_disconT = r_disconT
        self.conN = conN
        self.flag = flag

def data_udpate_view(request):

    # false - disconnected, true-connected
    flag = None
    l = []

    app_id = request.GET.get('id')
    app = InternalApp.objects.filter(id=app_id)

    if len(app) == 0:
        return Http404("THERE IS NO SUCH INTERNAL APPLICATION")
    header = 'Application ' + str(app_id) + '. ' + app[0].name
    # список из уникальных id абонентов, которые общались/общаются с данным приложением
    a = list(set(AbonentConnectionMetric.objects.filter(app_id=app_id).values_list('abonent__id', flat=True)))
#
    for id in a:
        time_of_disconnection = None
        time_without_connection = None
        time_with_connection = None
        time_of_connection = None

        ab = ExternalApp.objects.filter(id=id)
        if len(ab) != 0:
            ab = ab[0]
        else:
            continue

        # список из метрик пары InternalApp-ExternalApp, в порядке удаления по времени
        metrics_set = AbonentConnectionMetric.objects.filter(abonent__id=id).order_by('-sendTime')
        conN = metrics_set[0].connections_number
        if conN == 0:
            # нет соединения
            flag = False
#
            for i in range(len(metrics_set)):
                if metrics_set[i].connections_number != 0:
                    # момент разрыва
                    sent = metrics_set[i].sentBytes
                    recv = metrics_set[i].receivedBytes
                    time_of_disconnection = metrics_set[i].sendTime
                    break
            # if time_of_disconnection == None:
            #     print("[E] NO INFO ABOUT TIME OF DISCONNECTION")
            #     continue
            # else:
            now = datetime.now()
            now_secondsSinceEpoch = tt.mktime(now.timetuple())

            discon_secondsSinceEpoch = tt.mktime(time_of_disconnection.timetuple())

            c = now_secondsSinceEpoch - discon_secondsSinceEpoch
            s = c%60
            m = (c%3600 - s) // 60
            h = (c % 86400 - m) // 3600
            d = c // 86400

            time_without_connection =str(int(d)) + "d  " + str(int(h))+':'+str(int(m))+':'+str(int(s))
        else:
            flag = True
            time_of_connection = metrics_set[0].timeCon

            h = 0
            m = 0
            s = 0

            now = datetime.now()
            now_secondsSinceEpoch = tt.mktime(now.timetuple())

            discon_secondsSinceEpoch = tt.mktime(time_of_disconnection.timetuple())
            c = now_secondsSinceEpoch - discon_secondsSinceEpoch
            s = c % 60
            m = (c % 3600 - s) // 60
            h = (c % 86400 - m) // 3600
            d = c // 86400
            time_with_connection =str(int(d)) + "d  " + str(int(h))+':'+str(int(m))+':'+str(int(s))
            sent = metrics_set[0].sentBytes
            recv = metrics_set[0].receivedBytes
        result = {'abonent':ab.name, 'sentB':sent,'recvB':recv,'conT':time_of_connection, 'disconT':time_of_disconnection,'r_conT':time_with_connection,'r_disconT':time_without_connection,'conN':conN,'flag':flag}
        l.append(result)
    resp = {'res_list':l}

    return JsonResponse(resp)

def main_2(request, app_id):
    app = InternalApp.objects.filter(id=app_id)
    header = 'Application ' + str(app_id) + '. ' + app[0].name
    t = get_template('internal_apps_set/app_frame.html')
    html = t.render(Context({'header':header}))
    return HttpResponse(html)