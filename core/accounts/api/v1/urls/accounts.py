from django.urls import path, include
from accounts.api.v1 import view
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

urlpatterns = [
    path(
        "registrations/",
        view.RegestrationsApiView.as_view(),
        name="registrations",
    ),
    path(
        "token/create/",
        view.CustomCreateTokenApiView.as_view(),
        name="create-token",
    ),
    path(
        "token/discard/",
        view.CustomDiscardTokenApiView.as_view(),
        name="discard-token",
    ),
    path(
        "jwt/create/",
        view.CustomCreateJwtTokenApiView.as_view(),
        name="create-jwt-token",
    ),
    path("jwt/verify/", TokenVerifyView.as_view(), name="verify-jwt-token"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="refresh-jwt-token"),
    path(
        "changepassword/",
        view.ChangePasswordApiView.as_view(),
        name="change-password",
    ),
    path(
        "activations/confirm/<str:token>",
        view.ActivationsConfirmApiView.as_view(),
        name="activations",
    ),
    path(
        "activations/resend/",
        view.ActivationsRecendApiView.as_view(),
        name="activation-resend",
    ),
    path(
        "api/password_reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
]
