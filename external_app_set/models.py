from django.db import models

class ExternalApp(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.TextField()


    def __str__(self):
        return self.name
# Create your models here.
