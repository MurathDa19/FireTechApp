from difflib import restore
from django.shortcuts import render, redirect
from django.contrib import messages
from firebase_admin import firestore, auth
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from FireTech.firebase_conex import initialize_firebase


# Create your views here.

db = initialize_firebase()
def index(request):
    return render(request, 'index_user_view.html')


def Registro(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = auth.create_user_with_email_and_password(email, password)
            messages.success(request, 'Usuario registrado exitosamente')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Error al registrar el usuario: {e}')

    return render(request, 'registro.html')

def Login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = auth.sign_in_with_email_and_password(email, password)
            request.session['uid'] = user['localId']
            messages.success(request, 'Inicio de sesión exitoso')
            return redirect('index.html')
        except Exception as e:
            messages.error(request, f'Error al iniciar sesión: {e}')

    return render(request, 'login.html')

@user_passes_test(lambda u: u.is_superuser)
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

# @login_required_firebase
@user_passes_test(lambda u: u.is_superuser)
def Actualizar_mobile(request, mobil_id):
    """
    Docstring for actualizar_mobil
    UPDATE: Actualizar un documento específico de la colección 'mobil' en Firestore.
    """

    uid = request.session.get('uid')
    mobil_ref = db.collection('mobiles').document(mobil_id)

    try:
        doc = mobil_ref.get() #Obtenemos el documento de la coleccion mobiles
        if not doc.exists:
            messages.error(request, 'El Dispositivo no existe')
            return redirect('Listar_mobiles')
        mobil_data = doc.to_dict()
        if mobil_data.get('usuario_id') != uid:
            messages.error(request, ' ❌  No tienes permiso para editar este Dispositivo')
            return redirect('Listar_mobiles')
        mobil_ref.update({
            'marca': request.POST.get('marca'),
            'modelo': request.POST.get('modelo'),
            'precio': float(request.POST.get('precio')),
            'fecha_actualizacion' : firestore.SERVER_TIMESTAMP()
        })
        messages.success(request, '✅  Dispositivo actualizado exitosamente')
        return redirect('Listar_mobiles')
    except Exception as e:
        messages.error(request, f'❌  Error al alctualizar el Dispositivo: {e}')
        return redirect('Listar_mobiles')


def Listar_mobiles(request):
    """
    Listar todas las mobiles de Firestore.
    READ Action
    """
    # Obtener el UID del usuario de la sesión
    mobiles = []

    try:
        # Recuperar todas las mobiles del usuario actual
        docs = db.collection('mobiles').stream()
        for doc in docs:
            mobile = doc.to_dict()
            mobile['id'] = doc.id
            mobiles.append(mobile)
    except Exception as e:
        messages.error(request, f"|❌| Error al recuperar mobiles de Firestore: {e}")
    return render(request, "Mobiles/listar_mobiles.html", {'mobiles': mobiles})

@user_passes_test(lambda u: u.is_superuser)
def Eliminar_mobile(request, mobil_id):
    """
    Eliminar una tarea de Firestore. Se elimina el documento que contiene la tarea con el ID especificado.
    DELETE Action
    """
    try:
        # Eliminar la tarea de Firestore
        db.collection('mobiles').document(mobil_id).delete()
        messages.success(request, "|✅| Dispositivo móvil eliminado exitosamente")
    except Exception as e:
        messages.error(request, f"|❌| Error al eliminar dispositivo móvil en Firestore: {e}")
    return redirect('listar_mobiles')
