from django.db import models
from abonents.models import Abonent
from internal_apps_set.models import InternalApp

class Error_Metric(models.Model):
    abonent = models.ForeignKey(Abonent)
    importance_level = models.PositiveSmallIntegerField()
    app = models.ForeignKey(InternalApp)
    subprocess = models.TextField()
    description = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
# Create your models here.
