from django.urls import path
from .views import add_subject, view_subjects, update_enrollment,add_to_enrollment,view_all_subjects

urlpatterns = [
    path('add-subject/', add_subject, name='add-subject'),
    path('view-all-subjects/', view_all_subjects, name='view-subjects'),
    path('view-subjects/<int:user_id>/', view_subjects, name='view-subjects'),
    path('update-enrollment/<int:enrollment_id>/', update_enrollment, name='update-enrollment'),
    path('add-to-enrollment/<int:user_id>/', add_to_enrollment, name='add-to-enrollment')
]