from django.shortcuts import render
from FireTech.firebase_conex import initialize_firebase

# Create your views here.

db = initialize_firebase()
def index(request):
    return render(request, 'index.html')

@login_required_firebase
def actualizar_mobil(request, mobil_id):
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
            'fecha_actualizacion' : datetime.now()
        })
        messages.success(request, '✅  Dispositivo actualizado exitosamente')
        return redirect('Listar_mobiles')
    except Exception as e:
        messages.error(request, f'❌  Error al alctualizar el Dispositivo: {e}')
        return redirect('Listar_mobiles')
