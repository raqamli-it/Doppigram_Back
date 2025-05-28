from rest_framework import serializers
from .models import User

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=5)

class UserProfileSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'image']

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'phone', 'image']
