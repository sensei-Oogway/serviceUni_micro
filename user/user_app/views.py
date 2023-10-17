from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

class UserRegistration(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Extract user data from the request
            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')
            email = request.data.get('email')
            password = request.data.get('password')

            # Create a new User instance and associate it with the Cart
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLogin(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Check if the user with the given email and password exists
        try:
            user = User.objects.get(email=email, password=password)
        except User.DoesNotExist:
            return Response({"message": "Login failed. Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)

        # Serialize the user data and return it in JSON
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)