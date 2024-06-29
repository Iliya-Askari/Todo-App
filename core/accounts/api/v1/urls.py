from django.urls import path
from . import view
from rest_framework_simplejwt.views import TokenRefreshView , TokenVerifyView
urlpatterns =[
    path('regstrations/',view.RegestrationsApiView.as_view(),name='regstrations'),
    path('token/create/',view.CustomCreateTokenApiView.as_view(),name='crate-token'),
    path('token/discrad/',view.CustomDiscardTokenApiView.as_view(),name='discard-token'),
    path('jwt/create/',view.CustomCreateJwtTokenApiView.as_view(),name='create-jwt-token'),
    path('jwt/verify/',TokenVerifyView.as_view(),name='verify-jwt-token'),
    path('jwt/refresh/',TokenRefreshView.as_view(),name='refresh-jwt-token'),
    path('profile/',view.ProfileApiView.as_view(),name='profile-detail')
]