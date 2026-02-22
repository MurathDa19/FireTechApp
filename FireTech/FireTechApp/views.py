from pyexpat.errors import messages

from django.shortcuts import render
from django.shortcuts import render, redirect
from FireTech.firebase_conex import initialize_firebase
from django.contrib import messages




# Create your views here.

db = initialize_firebase()
def index(request):
    return render(request, 'index.html')


def Listar_mobiles(request):
    """
    READ: recuperar las tareas dle usuario desde firebase 

    """
    
    
    mobiless = []
    try:
        #vamos a filtrar las tareas por el UID del usuario
        docs = db.collection('mobiles').stream()
        for doc in docs:
            mobiles = doc.to_dict()
            mobiles['id'] = doc.id  # Agregar el ID del documento a los datos del móvil
            mobiless.append(mobiles)
            print(mobiles)
    except Exception as e:
        messages.error(request, f"Error al cargar los móviles: {e}")
    return render(request, 'Listar_mobiles.html', {'mobiles': mobiless})
def Crear_mobile(request):
    if request.method == 'POST':
        
        nombre = request.POST['nombre']
        marca = request.POST['marca']
        modelo = request.POST['modelo']
        color = request.POST['color']
        
        try:
            
            db.collection('mobiles').add({
                'nombre': nombre,
                'marca': marca,
                'modelo': modelo,
                'color': color,

            })
            messages.success(request, '|✅| Mobile creado exitosamente')
            return redirect('Listar_mobiles')
        except Exception as e:
            messages.error(request, f" |❌| Error al crear el mobile: {e}")
            return render(request, 'Mobiles/Crear_mobiles.html', {'message': 'Error al crear el mobile'})
    return render(request, 'Mobiles/Crear_mobiles.html')
