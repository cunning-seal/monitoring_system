from django.db import models
from abonents.models import Abonent
# пока вопросы по поводу идентификации, след.сем
class InternalApp(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.TextField(max_length=50)
    abonent = models.ForeignKey(Abonent)

    def __str__(self):
        return self.name