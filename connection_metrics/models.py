from django.db import models
from external_app_set.models import ExternalApp
from internal_apps_set.models import InternalApp

class AbonentConnectionMetric(models.Model):
    connections_number = models.PositiveSmallIntegerField()
    receivedBytes = models.BigIntegerField()
    sentBytes = models.BigIntegerField()
    abonent = models.ForeignKey(ExternalApp)
    sendTime = models.DateTimeField(auto_now_add=True)
    app = models.ForeignKey(InternalApp)
    timeCon = models.DateTimeField()

# Create your models here.
