from django.shortcuts import render
from .models import Planilla

def lista_planilla(request):
    # Obtener todos los registros de la tabla 'planilla'
    datos = Planilla.objects.all()
    # Renderizar la plantilla HTML con los datos
    return render(request, 'planilla/lista.html', {'datos': datos})  
