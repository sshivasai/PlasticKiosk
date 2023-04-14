from django.urls import path
from . import views

urlpatterns = [

    path('pricelists_details/<str:name>/', views.pricelists_details, name='pricelists_details'),
]
