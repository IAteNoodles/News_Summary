from django.shortcuts import render
from rest_framework import generics
from .serializers import UserRegistrationSerializer
from rest_framework.permissions import AllowAny

# Create your views here.

class UserRegistrationView(generics.CreateAPIView):
    """
    An endpoint for registering a new user.
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)
