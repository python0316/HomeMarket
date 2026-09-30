from rest_framework import serializers
from realestate.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True)

  class Meta:
    model = User
    fields = [
        'id',
        'username',
        'password',
        'phone_number',
        'passport_number',
        'address',
    ]

  def create(self, validated_data):
    password = validated_data.pop('password')
    user = User(**validated_data)
    user.set_password(password)  # Parolni shifrlash
    user.is_client = True
    user.save()
    return user