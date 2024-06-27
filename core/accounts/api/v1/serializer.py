from rest_framework import serializers
from typing import Any, Dict
from django.contrib.auth import get_user_model , authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class RegestrationsSerializer(serializers.ModelSerializer):
    password_2 = serializers.CharField(max_length=255 , write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password', 'password_2']

    def validate(self, attrs):
        if attrs.get('password_2') != attrs.get('password'):
            raise serializers.ValidationError(_('Passwords must match'))
        try:
            validate_password(attrs.get('password'))
        except serializers.ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})
        return super().validate(attrs)
    
    def create(self, validated_data):
        validated_data.pop('password_2', None)
        return User.objects.create_user(**validated_data)