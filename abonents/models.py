from django.db import models

class Abonent(models.Model):
    # внешний ключ абонента
    computer_id = models.BigIntegerField(primary_key=True)
    # полное название или описание машины
    name = models.TextField(max_length=50)

    def __str__(self):
        return self.name

# Create your models here.
