from django.urls import path
from . import view

urlpatterns =[
    path('regstrations/',view.RegestrationsApiView.as_view(),name='regstrations'),
    path('token/create/',view.CustomLoginTokenApiView.as_view(),name='crate-token')
]