from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse
from django.template import Context

def main_view(request):
    greetings = "Greetings, stranger!!!"

    t = get_template('../../mainpage/templates/mainpage/index.html')
    html = t.render(Context({'greetings':greetings}))

    return HttpResponse(html)
# Create your views here.
