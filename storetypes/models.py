from django.db import models

# Create your models here.
class storetypes(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200,blank=True,null=True)

    class Meta:
        verbose_name = 'Store Type'
        verbose_name_plural = 'Store Types'
    def __str__(self):
        return self.name