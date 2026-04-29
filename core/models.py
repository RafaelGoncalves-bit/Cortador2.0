from django.db import models

class CortadorModel(models.Model):
    numero = models.CharField(max_length=50)
    dataRecarga = models.DateField(auto_now=True)
