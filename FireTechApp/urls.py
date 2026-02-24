from FireTechApp import views
from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('crear_mobile/', views.Crear_mobile, name='crear_mobile'),
    path('actualizar_mobile/<str:mobil_id>/', views.Actualizar_mobile, name='actualizar_mobile'),
    path('listar_mobile/', views.Listar_mobiles, name='listar_mobile'),
    path('eliminar_mobile/<str:mobil_id>/', views.Eliminar_mobile, name='eliminar_mobile'),
    path('registro/', views.Registro, name='registro'),
    path('login/', views.Login_view, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),


    
]
