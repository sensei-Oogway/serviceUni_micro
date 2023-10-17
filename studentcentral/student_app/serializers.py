from rest_framework import serializers
from .models import Subject, Enrollment


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['subject_code', 'name', 'details']  # Include subject_code and details



class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'  



