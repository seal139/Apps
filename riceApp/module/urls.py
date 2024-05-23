from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('module/', views.index, name='module'),
    path('api/<slug:command>/', api.api),
]