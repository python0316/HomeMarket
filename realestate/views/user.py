from rest_framework import generics, permissions
from realestate.models import User
from realestate.serializers import UserRegisterSerializer


class RegisterAPIView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserRegisterSerializer
  permission_classes = [permissions.AllowAny]  # Hamma ro'yxatdan o'ta oladi