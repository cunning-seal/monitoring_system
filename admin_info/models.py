from django.db import models

class BrokenPackage(models.Model):
    data = models.TextField()
    sendTime = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    code = models.PositiveIntegerField(default=0)

# Create your models here.
