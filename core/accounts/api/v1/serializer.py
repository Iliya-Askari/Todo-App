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
        fields = ['email', 'password', 'password_2']

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
    
class CustomLoginTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("email"),write_only=True)
    password = serializers.CharField(label=_("Password"),style={'input_type': 'password'},trim_whitespace=False,write_only=True)
    token = serializers.CharField(label=_("Token"),read_only=True)

    def validate(self, attrs):
        username = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')
        if username and password :
            user = authenticate(request=request,username=username, password=password)
            if not user:
                raise serializers.ValidationError(_('Invalid credentials'))
        else :
            raise serializers.ValidationError(_('email and password required'))

        attrs['user'] = user
        return attrs
    