from FireTechApp import views
from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('Crear_mobiles/', views.Crear_mobile, name='Crear_mobiles'),
]
