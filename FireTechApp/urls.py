from FireTechApp import views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('crear_mobile/', views.Crear_mobile, name='crear_mobile'),
]
