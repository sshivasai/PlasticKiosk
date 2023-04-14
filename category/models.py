from django.db import models
from django.urls import reverse
# Create your models here.
class category(models.Model):
    choices_id = (
        (1,'HouseHold'),
        (2,'Small Scale Industry' )
    )
    choices_name = (
        ('HouseHold','HouseHold'),
        ('Small Scale Industry','Small Scale Industry' )
    )
    #small scale and retailer refer same
    name = models.CharField(max_length=50,choices=choices_name)
    description = models.CharField(max_length=200,blank=True,null=True)
    image = models.ImageField(upload_to='photos/category')
    cat_id = models.IntegerField(choices=choices_id)

    #if  cat_id == '1 for HouseHold':
    #    cat_id == 1
    #else:
    #     cat_id == 2

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    def __str__(self):
        return self.name
    def get_url(self):
        return reverse('pricelists_details',args= [str(self.name)])

    def get_url_category(self):
        return reverse('productbycategory',args= [str(self.name)])
    
    
    