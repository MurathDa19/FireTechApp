from django.shortcuts import render, redirect
from FireTech.firebase_conex import initialize_firebase
from django.contrib import messages




# Create your views here.

db = initialize_firebase()
def index(request):
    return render(request, 'index.html')

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
