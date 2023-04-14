from django.db import models
from category.models import category
from pricelists.models import pricelists as p
from django.urls import reverse
# Create your models here.
class Product(models.Model):
    product_name    = models.CharField(max_length=200, unique=True)
    description     = models.TextField(max_length=500, blank=True)
    price           = models.ForeignKey(p, on_delete=models.CASCADE)
    image          = models.ImageField(upload_to='photos/products')
    current_stock   = models.IntegerField()

    def __str__(self):
        return self.product_name + "-" + str(self.price.category) +" @ "+ str(self.price.price_per_pound) + "$"

    def category(self):
        return self.price.category

    def get_url_category(self):
        return reverse('productbycategory',args= [str(self.price.category)])

        
    def get_url_name(self):
        return reverse('productbyname',args= [str(self.product_name)])
