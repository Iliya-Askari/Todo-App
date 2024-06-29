from django.urls import path
from . import view

urlpatterns =[
    path('regstrations/',view.RegestrationsApiView.as_view(),name='regstrations'),
    path('token/create/',view.CustomCreateTokenApiView.as_view(),name='crate-token'),
    path('token/discrad/',view.CustomDiscardTokenApiView.as_view(),name='discard-token'),
]