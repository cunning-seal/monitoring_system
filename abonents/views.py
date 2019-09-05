from django.http import HttpResponse, Http404, JsonResponse
from django.template.loader import get_template
from django.template import Context
from abonents.models import Abonent
from hardware_metrics.models import Total_Hardware_Metric
from error_packages.models import Error_Metric
from internal_apps_set.models import InternalApp

def main_view(request):
    abonents_list = Abonent.objects.order_by('computer_id')
    t = get_template('abonents/index.html')
    html = t.render(Context({'abonents_list': abonents_list}))
    return HttpResponse(html)

def abonent_view(request, abonent_id):
    metrics_list = Total_Hardware_Metric.objects.filter(abonent__computer_id=abonent_id).order_by('-time')[:10]
    ab_name = Abonent.objects.filter(computer_id=abonent_id)[0].name
    t = get_template('abonents/hw.html')
    apps_list = InternalApp.objects.filter(abonent__computer_id=abonent_id)
    html = t.render(Context({'metrics_list':metrics_list, 'id':abonent_id, 'apps_list':apps_list, 'name':ab_name, 'last_rec_id':0}))
    return HttpResponse(html)

def error_view(request, abonent_id):
    metrics_list = Error_Metric.objects.filter(abonent__computer_id=abonent_id).order_by('-time')
    t = get_template('abonents/error.html')

    html = t.render(Context({'metrics_list':metrics_list, 'id':abonent_id,}))
    return HttpResponse(html)

def update_view(request):
    l = []
    record_id = request.GET.get('last_rec_id')
    computer_id = request.GET.get('id')
    ab_name = Abonent.objects.get(computer_id=computer_id).name
    metric_list = Total_Hardware_Metric.objects.filter(abonent__computer_id=computer_id).order_by('-time')
    if len(metric_list) == 0:
        resp = {'name':ab_name, 'list':[], 'lri':record_id}
        return JsonResponse(resp)
    if record_id == -1:
        for metric in metric_list:
            t = metric.temperature
            cpu = metric.total_CPU_load
            time = metric.time
            r = {'t': t, 'cpu': cpu, 'time_c': time}
            l.append(r)
            resp = {'name': ab_name, 'list': l, }
            return JsonResponse(resp)
    if record_id == metric_list[0].id:
        resp = {'name':ab_name, 'list':[], 'lri':record_id}
        return JsonResponse(resp)
    result = metric_list.filter(id__gt = record_id)
    if(len(result) == 0):
        resp = {'name': ab_name, 'list': [], 'lri': record_id}
        return JsonResponse(resp)

    for metric in result:
        t = metric.temperature
        cpu = metric.total_CPU_load
        time = metric.time
        r = {'t':t, 'cpu':cpu, 'time_c':time}
        l.append(r)
    lri = result[0].id
    resp = {'name':ab_name, 'list':l, 'lri':lri}
    return JsonResponse(resp)
# Create your views here.

def graph_view(request, abonent_id):

    t = get_template('abonents/graph.html')

    html = t.render(Context({'abonent_id': abonent_id}))
    return HttpResponse(html)

