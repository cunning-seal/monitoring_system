from django.db import models
from abonents.models import Abonent
# class ClientDBMetric(models.Model):
#     client_id = models.TextField


class ServerDBMetric(models.Model):
    db_abonent = models.ForeignKey(Abonent)
    db_work_status = models.BooleanField()
    max_connections_number = models.PositiveIntegerField()
    connections_number = models.PositiveIntegerField()
    rollback_percent = models.FloatField()
    database_size = models.FloatField()
    time = models.DateTimeField(auto_now_add=True, )

# Create your models here.
