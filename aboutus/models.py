from django.db import models

# Create your models here.
class aboutus(models.Model):
    name = models.CharField(max_length=200);
    subtext = models.CharField(max_length=200,null=True,blank=True);
    aboutus = models.CharField(max_length=3000);
    fb_link = models.CharField(max_length=200,null=True,blank=True);
    ig_link = models.CharField(max_length=200,null=True,blank=True);
    twitter_link = models.CharField(max_length=200,null=True,blank=True);
    contact_no = models.CharField(max_length=12,blank=True,null=True)
    email_id = models.EmailField(max_length=200,blank=True,null=True)
    location = models.CharField(max_length=250,null=True)
    class Meta:
        verbose_name = 'about us'
        verbose_name_plural = 'about us'

    def __str__(self):
        return "about us " + str(self.name)