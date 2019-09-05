from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, JsonResponse
from error_packages.models import Error_Metric


def main_view(request):
    t = get_template('error_packages/index.html')
    html = t.render(Context({'last_rec_id': 0}))
    return HttpResponse(html)

# Create your views here.

def er_update_view(request):

    record_id = request.GET.get('last_rec_id')
    metric_list = Error_Metric.objects.filter(id__gt=record_id).order_by('-time')
    if(len(metric_list)==0):
        resp = {
            'response': [],
            'lri': record_id
        }
        return JsonResponse(resp)
    lri = metric_list[0].id
    # if(record_id == lri):
    #     resp = {
    #         'response': [],
    #         'lri': record_id
    #     }
    ans = []
    for metric in metric_list:
        ab_id = metric.abonent.computer_id
        ab_name = metric.abonent.name
        app_id = metric.app.id
        app_name = metric.app.name
        i_level = metric.importance_level
        subprocess = metric.subprocess
        descr = metric.description
        time = metric.time
        res = {'ab_id':ab_id,'ab_name':ab_name,'app_id':app_id,'app_name':app_name, 'i_level':i_level,
               'subprocess':subprocess,'descr':descr, 'time':time}
        ans.append(res)
    resp = {
        'response':ans,
        'lri':lri
    }
    return JsonResponse(resp)