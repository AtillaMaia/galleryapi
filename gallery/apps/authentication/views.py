from django.contrib.auth import login, logout
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import RegisterSerializer, \
    LoginSerializer, LogoutSerializer


class RegisterView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(responses={status.HTTP_201_CREATED: ''})
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        login_serializer = self.serializer_class(data=request.data)
        login_serializer.is_valid(raise_exception=True)

        user = login_serializer.validated_data['user']
        login(request, user)

        return Response(login_serializer.data, status=status.HTTP_200_OK)


class LogoutView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(responses={status.HTTP_200_OK: ''})
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            logout(request)
        except TokenError:
            return Response({'error': 'Token is expired or invalid.'},
                status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_204_NO_CONTENT)