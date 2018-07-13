from django.urls import path
from . import views

urlpatterns = [
    path('', views.PollView.as_view(), name='index')
]

