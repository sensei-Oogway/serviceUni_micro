from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegistration.as_view(), name='user-registration'),
    path('login/', views.UserLogin.as_view(), name='user-login'),
]

