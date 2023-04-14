from django.contrib import admin

# Register your models here.
from .models import pricelists

class pricelistsAdmin(admin.ModelAdmin):
    list_display = ('name','category','price_per_pound',)
# Register your models here.
admin.site.register(pricelists,pricelistsAdmin)