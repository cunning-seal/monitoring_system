#from django.apps import AppConfig

import django.apps
import re
import socket, struct
from django.dispatch import Signal, receiver


# on_active = Signal(providing_args=['flag'])

class MyAppConfig(django.apps.AppConfig):
    name = 'receiver_app'
    path = '/home/artyom/firstsite/receiver_app'
    def ready(self):
      pass
