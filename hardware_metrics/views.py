from django.template.loader import get_template

from django.template import Context
from django.http import HttpResponse, Http404, JsonResponse
from .models import Total_Hardware_Metric
from abonents.models import Abonent

def main_view(request):
    # переделаю в последнюю метрику для абонента
    # проблемесы - distinct() работает только в PostgreSQL (ну и фиг с ним)
    metric_list = []
    ab_list = Abonent.objects.all()
    for ab in ab_list:
        metric = Total_Hardware_Metric.objects.filter(abonent__computer_id=ab.computer_id).order_by('-time')
        if len(metric) != 0:
            metric_list.append(metric[0])

    t = get_template('hardware_metrics/index.html')
    html = t.render(Context({'metric_list':metric_list}))
    return HttpResponse(html)

def graph_view(request):
    try:
        f = open('./static/hardware_metrics/data.txt','w')
    except:
        print("Problems with importing file")
        return Http404

    #TODO try-catch прописать
    t = get_template('hardware_metrics/graph.html')
    html = t.render()
    m_list = Total_Hardware_Metric.objects.order_by('time')[:10]
    for record in m_list:
        temperature = record.temperature
        time = record.time.isoformat()
        str_repr = str(time) + ',' + str(temperature)
        print(str_repr)
        f.write(str_repr)
    f.close()
    return HttpResponse(html)

def main_ajax_update_view(request):
    metrics_list = request.GET['metrics_list']
    # обновленная информация по уже отображенным (чтобы не двигались)
    update_list = []
    # метрики по новым абонентам
    new_abonents_list = []
    ab_list = Abonent.objects.all()
    for metric in metrics_list:
        flag = 0
        up_metric = Total_Hardware_Metric.objects.filter(abonent__computer_id=metric.computer_id).order_by('-time')
        for ab in ab_list:
            if(ab.computer_id == metric.abonent.computer_id):
                ab_list = ab_list.exclude(computer_id=ab.computer_id)
                break
        if len(up_metric) != 0:
            update_list.append(up_metric[0])
    for ab in ab_list:
        new_ab_metric = Total_Hardware_Metric.objects.filter(abonent__computer_id=ab.computer_id).order_by('-time')
        if len(new_ab_metric) != 0:
            new_abonents_list.append(new_ab_metric)

    data = {'new_ab_m':new_abonents_list, 'up_metrics':update_list}

    return JsonResponse(data)