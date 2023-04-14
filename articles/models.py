from django.db import models
from category.models import category
from django.urls import reverse
# Create your models here.
class blog(models.Model):
    blog_title = models.CharField(max_length= 2000)
    category = models.ForeignKey(category,on_delete=models.CASCADE,blank=True,null=True)
    paragraph_1 = models.CharField(max_length=20000,)
    paragraph_2 = models.CharField(max_length=20000,blank=True)
    paragraph_3 = models.CharField(max_length=20000,blank=True)
    paragraph_4 = models.CharField(max_length=20000,blank=True)
    author = models.CharField(max_length=50,blank=True)
    image_1 = models.ImageField(upload_to='photos/articles')
    created_date = models.DateField(auto_now_add=True)
    last_modified_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.blog_title

    def get_url(self):
        return reverse('article_details',args= [str(self.blog_title)])
        
 