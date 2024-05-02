from django.urls import path
from . import views

urlpatterns = [
    path('module/', views.members, name='module'),
]