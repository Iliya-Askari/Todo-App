from django.urls import path
from . import view

urlpatterns =[
    path('regstrations/',view.RegestrationsApiView.as_view(),name='regstrations')
]