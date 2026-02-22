from difflib import restore
from django.shortcuts import render, redirect
from django.contrib import messages
from firebase_admin import firestore
from django.contrib.auth import login, logout, authenticate
from FireTech.firebase_conex import initialize_firebase

# Create your views here.

db = initialize_firebase()
def index(request):
    return render(request, 'index.html')

def Crear_mobile(request):
    """
    Crear un nuevo dispositivo móvil en Firestore.
    CREATE Action
    """

    if request.method == 'POST':
        # Recuperar los datos del formulario
        nombre = request.POST.get('nombre')
        modelo = request.POST.get('modelo')
        marca = request.POST.get('marca')
        precio = request.POST.get('precio')

        try:
            db.collection('mobiles').add({
                'nombre': nombre,
                'modelo': modelo,
                'marca': marca,
                'precio': precio,
                'fecha_creacion': firestore.SERVER_TIMESTAMP
            })
            messages.success(request, "|✅| Dispositivo móvil creado exitosamente")
            return redirect('listar_mobiles')
        except Exception as e:
            messages.error(request, f"|❌| Error al crear dispositivo móvil en Firestore: {e}")

    return render(request, 'Mobiles/crear_mobile.html')
