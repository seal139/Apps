from django.urls import path
from . import views

urlpatterns = [
    path('module/', views.index, name='module'),
]