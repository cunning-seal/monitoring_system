from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from database_metrics.models import ServerDBMetric
from django.template import Context
from django.core import serializers
from django.utils.dateparse import parse_date

def main_view(request):
    metric_list = ServerDBMetric.objects.order_by('-time')
    t = get_template('database_metrics/index.html')
    html = t.render(Context({'metric_list': metric_list}))
    return HttpResponse(html)
# Create your views here.

def update_view(request):
    record_id = parse_date(request.GET.get('id'))
    metric_list = ServerDBMetric.objects.filter(id__gt=record_id).order_by('-time')
    print(metric_list)
    data = serializers.serialize('json', metric_list)
    return JsonResponse(data)
