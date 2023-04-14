from django.urls import path
from . import views


urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('payments/', views.payments, name='payments'),
    path('order_complete/', views.order_complete, name='order_complete'),
    path('order_complete_house/<int:order_number>/', views.order_complete_house, name='order_complete_house'),
path('order_complete_small/<int:order_number>/', views.order_complete_small, name='order_complete_small'),
]
