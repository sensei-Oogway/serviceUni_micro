from django.urls import path
from . import views
from .views import book_appointment, view_slots, view_appointments, update_appointment,add_gp,get_all_gp,update_gp

urlpatterns = [
    path('book-appointment/', book_appointment, name='book-appointment'),
    path('view-slots/<int:gp_id>/', view_slots, name='view-slots'),
    path('view-appointments/<int:user_id>/', view_appointments, name='view-appointments'),
    path('update-appointment/<int:gp_id>/<int:appointment_id>/', update_appointment, name='update-appointment'),
    path('add-gp/', add_gp, name='add-gp'),
    path('get-all-gp/',get_all_gp , name='get_all_gp'),
    path('update-gp/<int:id>/', update_gp, name='update-gp'),
    path('view-gp/<int:id>/', views.ViewGP.as_view(), name='view-gp'),
]
