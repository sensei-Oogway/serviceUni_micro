from django.urls import path
from . import views

from .views import get_medicine_details, add_medicine, get_all_medicines
urlpatterns = [
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('view-cart/<int:cart_id>/', views.view_cart, name='view-cart'),
    path('update-cart/<int:cart_id>/', views.update_cart, name='update-cart'),
    path('get-cart/<int:cart_id>/', views.GetCart.as_view(), name='get-cart'),
    
    path('get-medicine-details/<int:medicine_id>/', get_medicine_details, name='get-medicine-details'),
    path('add-medicine/', add_medicine, name='add-medicine'),
    path('get-all-medicines/', get_all_medicines, name='get-all-medicines')
]
