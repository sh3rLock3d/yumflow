from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import ValidationError


# User Serializer
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(
    validators=[UniqueValidator(queryset=User.objects.all())]
  ) 
  
  class Meta:
    model = User
    fields = ('id', 'username', 'email', 'password')
    extra_kwargs = {'password': {'write_only': True}}

  def validate_password(self, data):
    if data.isdigit():
      raise ValidationError('رمز باید شامل حروف نیز باشد')
    elif len(data) < 5:
      raise ValidationError('رمز باید بیشتر از ۵ کاراکتر باشد')
    return data

  def create(self, validated_data):
    user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

    return user

# Login Serializer
class LoginSerializer(serializers.Serializer):
  username = serializers.CharField()
  password = serializers.CharField()

  def validate(self, data):
    user = authenticate(**data)
    if user and user.is_active:
      return user
    raise serializers.ValidationError("اطلاعات ورودی اشتباه است.")