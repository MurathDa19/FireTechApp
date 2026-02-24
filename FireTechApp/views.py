from difflib import restore
from django.shortcuts import render, redirect
from django.contrib import messages
from firebase_admin import firestore, auth
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from datetime import datetime
import os
import requests

from FireTech.firebase_conex import initialize_firebase


# Create your views here.

db = initialize_firebase()
print("🔥 DB:", db)


def index(request):
    return render(request, 'index_user_view.html')


def Registro(request):
    mensaje = None

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('username')  # ✅ faltaba

        try:
            print("🚀 Creando usuario...")

            user = auth.create_user(
                email=email,
                password=password,
                display_name=username   # ✅ nombre correcto
            )

            print("✅ Usuario creado:", user.uid)

            db.collection('perfiles').document(user.uid).set({
                'email': email,
                'uid': user.uid,
                'username': username,
                'rol': 'aprendiz',
                'fecha_registro': datetime.now()
            })

            print("🔥 Documento Firestore creado")

            mensaje = f"Usuario {username} registrado exitosamente"
            return redirect('login')

        except Exception as e:
            print("❌ ERROR REAL:", e)
            messages.error(request, f'Error al registrar el usuario: {e}')

    return render(request, 'registro.html', {'mensaje': mensaje})

def Login_view(request):

    if 'uid' in request.session:
        return redirect('listar_mobiles')

    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')
        api_key = os.getenv('API_KEY')

        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"

        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }

        try:
            response = requests.post(url, json=payload)
            data = response.json()
            print("STATUS:", response.status_code)
            print("DATA:", data)
            print("API KEY:", api_key)
            print("API KEY SETTINGS:", os.getenv("FIREBASE_API_KEY"))

            
            if response.status_code == 200:
                request.session['uid']= data ['localId']
                request.session['email']= data ['email']
                request.session['idToken']= data ['idToken']
                messages.success(request,  f"Inicio de sesión exitoso para {email}")
                return redirect('listar_mobile')

            else:
                error_message = data.get ('error', {}).get('message', 'UNKNOWN_ERROR')

                errores_comunes= {
                    'INVALID_LOGIN_CREDENTIALS': 'La contraseña es incorrecta o el correo no es válido.',
                    'EMAIL_NOT_FOUND': 'Este correo no está registrado en el sistema.',
                    'USER_DISABLED': 'Esta cuenta ha sido inhabilitada por el administrador.',
                    'TOO_MANY_ATTEMPTS_TRY_LATER': 'Demasiados intentos fallidos. Espere unos minutos.'
                }
                mensaje_usuario = errores_comunes.get(error_message, 'Error desconocido. Inténtalo de nuevo.')
                messages.error(request, mensaje_usuario)
        except requests.exceptions.RequestException as e:
            messages.error(request,"Error de conexión: {e}") 
        except Exception as e:
            messages.error(request, f"Error inesperado: {str(e)}")
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


def cerrar_sesion(request):
    #Lo primero que toca hacer es limpiar la sesion y luego se redirige
    request.session.flush() # Limpia toda la sesión, eliminando todas las claves y valores asociados al usuario actual.
    messages.info(request, "✅ Sesión cerrada exitosamente.")
    return redirect('login')
