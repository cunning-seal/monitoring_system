from django.shortcuts import render
from django.template import Context
from django.template.loader import get_template
from django.http import HttpResponse,Http404
from external_app_set.models import ExternalApp

def main_view(request):
    app_list = ExternalApp.objects.all()

    t = get_template('external_app_set/index.html')

    html = t.render(Context({'apps_list':app_list}))
    return HttpResponse(html)
# Create your views here.
