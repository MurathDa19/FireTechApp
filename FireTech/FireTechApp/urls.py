from FireTechApp import views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Listar_mobiles/', views.Listar_mobiles, name='Listar_mobiles'),
]
