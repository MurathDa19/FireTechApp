from django.shortcuts import render
from FireTech.firebase_conex import initialize_firebase

# Create your views here.

db = initialize_firebase()
def index(request):
    return render(request, 'index.html')