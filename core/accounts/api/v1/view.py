from rest_framework import generics, views, permissions
from rest_framework.response import Response
from .serializer import *
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.authtoken.models import Token
from accounts.models import Profile
from django.shortcuts import get_object_or_404
from mail_templated import EmailMessage
from accounts.api.utils import EmailThread
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError

from decouple import config


class RegestrationsApiView(generics.GenericAPIView):
    serializer_class = RegestrationsSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegestrationsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data["email"]
            data = {"email": email}
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class CustomCreateTokenApiView(TokenObtainPairView):
    serializer_class = CustomCreateTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {"token": token.key, "user_id": user.pk, "email": user.email}
        )


class CustomDiscardTokenApiView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomCreateJwtTokenApiView(TokenObtainPairView):
    serializer_class = CustomCreateJwtTokenSerializer


class ProfileApiView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj


class ChangePasswordApiView(generics.GenericAPIView):
    model = get_user_model
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(
                serializer.data.get("old_password")
            ):
                return Response(
                    {"old_password": ["Wrong  password"]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            respone = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "password updated successfully",
                "data": [],
            }
            return Response(respone)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivationsConfirmApiView(views.APIView):
    """
    activate your account with email confirmation
    """

    def get(self, request, token, *args, **kwargs):
        try:
            token = jwt.decode(
                token, config("SECRET_KEY"), algorithms=["HS256"]
            )
            user_id = token.get("user_id")
        except ExpiredSignatureError:
            return Response(
                {"details": "token has been expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except InvalidSignatureError:
            return Response(
                {"details": "token is invalid"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_obj = User.objects.get(pk=user_id)
        if user_obj.is_verified:
            return Response({"details": "your account already been verified"})
        user_obj.is_verified = True
        user_obj.save()
        return Response(
            {
                "details": "your account been verified and activateions successfuly"
            }
        )


class ActivationsRecendApiView(generics.GenericAPIView):
    """
    send your email for verification
    """

    serializer_class = ActivsionRecendSerializer

    def post(self, request, *args, **kwargs):
        serializer = ActivsionRecendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data["user"]
        token = self.get_tokens_for_user(user_obj)
        emai_obj = EmailMessage(
            "email/activision_email.tpl",
            {"token": token},
            "user@example.com",
            to=[user_obj.email],
        )
        EmailThread(emai_obj).start()
        return Response({"details": "user activision recend successfully"})

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
