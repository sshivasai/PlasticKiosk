from django.urls import path
from . import views

urlpatterns = [

    path('category/<str:name>/products/', views.productbycategory, name='productbycategory'),
    path('products/<str:product_name>/', views.productbyname, name='productbyname'),
    
]
