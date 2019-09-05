from django.db import models
from abonents.models import Abonent

class Total_Hardware_Metric(models.Model):
    # внешний ключ на абонента
    abonent = models.ForeignKey(Abonent)
    # температура процессора
    temperature = models.DecimalField( max_digits=6, decimal_places=3)
    # загрузка процессора, в процентах
    total_CPU_load = models.DecimalField( max_digits=5, decimal_places=2)
    # время получения данных
    time = models.DateTimeField(auto_now_add=True,)

    def __str__(self):
        representation = str(self.abonent.computer_id) + " " + str(self.time)
        return representation

# Create your models here.
