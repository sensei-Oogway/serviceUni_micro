# serializers.py
from rest_framework import serializers
from .models import GP

class GpSerializer(serializers.ModelSerializer):
    class Meta:
        model = GP
        fields = '__all__'
