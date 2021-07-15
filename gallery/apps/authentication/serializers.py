from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class TokensSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(required=True, max_length=68,
                                     min_length=6,  write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, max_length=68,
                                     min_length=6,  write_only=True)
    tokens = serializers.SerializerMethodField(read_only=True)
    is_staff = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'password', 'tokens', 'is_staff']

    @swagger_serializer_method(serializer_or_field=TokensSerializer)
    def get_tokens(self, obj):
        return obj['user'].tokens()

    @swagger_serializer_method(serializer_or_field=serializers.BooleanField)
    def get_is_staff(self, obj):
        return obj['user'].is_staff

    def validate(self, attrs):
        user = authenticate(username=attrs['username'],
                            password=attrs['password'])
        if not user:
            raise AuthenticationFailed('Invalid credentials.')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled.')

        attrs['user'] = user
        return attrs


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def __init__(self, *args, **kwargs):
        super(LogoutSerializer, self).__init__(*args, **kwargs)
        self.token = None

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('Token is expired or invalid.')