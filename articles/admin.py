from django.contrib import admin
from articles.models import blog
# Register your models here.
class blogAdmin(admin.ModelAdmin):
    list_display = ('blog_title', 'category', 'created_date','last_modified_date')

admin.site.register(blog,blogAdmin)