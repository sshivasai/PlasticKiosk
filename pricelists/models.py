from django.db import models
from category.models import category as c
from django.urls import reverse

# Create your models here.
class pricelists(models.Model):

    name = models.CharField(max_length = 50)
    category = models.ForeignKey(c,on_delete=models.CASCADE)
    link = models.CharField(max_length=100,blank=True)
    description = models.CharField(max_length=255,blank = True)
    price_per_pound = models.FloatField(default=0)
    class Meta :
        verbose_name = 'Price List'
        verbose_name_plural = 'Prices List'

    def __str__(self):
        return self.name + " - " + str(self.category) + " @ "+ str(self.price_per_pound) + "$"
    