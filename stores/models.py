from django.db import models
from storetypes.models import storetypes
# Create your models here.


class stores(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    storetype = models.ForeignKey(storetypes,on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'Store'
        verbose_name_plural = 'Stores'
    def __str__(self):
        return str(self.name) + str(self.address)