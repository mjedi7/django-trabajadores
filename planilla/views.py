import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db.models import Count
from django.utils import timezone
from .models import Usuario, Planilla, Adscripcion, Plazas, Directorio

def login_usuario(request):
    mensaje = ''
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        contrasena = request.POST.get('contrasena')
        recordar = request.POST.get('recordar')

        try:
            user = Usuario.objects.get(nombre_usuario=usuario, contrasena=contrasena, estatus=True)
            user.ultimo_ingreso = timezone.now()
            user.save()

            response = redirect('planilla')
            max_age = 60*60*24*30 if recordar else None
            response.set_cookie('usuario', usuario, max_age=max_age)
            response.set_cookie('autorizacion', user.autorizacion, max_age=max_age)
            return response

        except Usuario.DoesNotExist:
            mensaje = 'Usuario o contraseña incorrectos, intenta nuevamente.'

    return render(request, 'planilla/login.html', {'mensaje': mensaje})

def logout_usuario(request):
    response = redirect('login_usuario')
    response.delete_cookie('usuario')
    response.delete_cookie('autorizacion')
    return response

def lista_planilla(request):
    datos = Planilla.objects.all()
    usuario_cookie = request.COOKIES.get('usuario', '')
    autorizacion = ''
    if usuario_cookie:
        usuario_obj = Usuario.objects.filter(nombre_usuario=usuario_cookie).first()
        if usuario_obj:
            autorizacion = usuario_obj.autorizacion

    return render(request, 'planilla/lista.html', {
        'datos': datos,
        'autorizacion_usuario': autorizacion,
    })

def lista(request):
    datos = Planilla.objects.all()
    return render(request, 'planilla/lista.html', {'datos': datos})

def plazas(request):
    return render(request, 'planilla/plazas.html')

def files(request):
    return render(request, 'planilla/files.html')

def test(request):
    return render(request, 'planilla/prueba.html')

def dplanteles(request):
    return render(request, 'planilla/debug_planteles.html')

def anexo_ejecucion(request):
    plazas = Plazas.objects.all()
    return render(request, 'planilla/anexo_ejecucion.html', {'plazas': plazas})

def historial(request):
    return render(request, 'planilla/historial.html')

def debug_planteles(request):
    planteles = Adscripcion.objects.filter(activo="1").order_by('nombre')
    return render(request, 'planilla/debug_planteles.html', {'planteles': planteles})

@csrf_exempt
def altas_nueva(request):
    if request.method == 'POST':
        nombre = f"{request.POST.get('nombre', '').strip()} {request.POST.get('apellido_paterno', '').strip()} {request.POST.get('apellido_materno', '').strip()}"
        plantel_id = request.POST.get('plantel', '')
        adscripcion_obj = Adscripcion.objects.filter(id=plantel_id).first()
        adscripcion_texto = adscripcion_obj.nombre if adscripcion_obj else ''
        departamento = adscripcion_obj.municipio if adscripcion_obj else ''
        clave = request.POST.get('no_personal', '').strip()

        if Planilla.objects.filter(clave=clave).exists():
            messages.error(request, '❌ Ya existe un registro con ese número de personal.')
            return redirect('altas_nueva')

        Planilla.objects.create(
            nombre=nombre,
            adscripcion=adscripcion_texto,
            departamento=departamento,
            clave=clave,
            rfc=request.POST.get('rfc', '').strip(),
            curp=request.POST.get('curp', '').strip(),
            puesto=request.POST.get('categoria', '').strip(),
            sindicato=request.POST.get('sindicalizado', '').strip(),
            fecha_de_ingreso=request.POST.get('fecha_ingreso', None)
        )

        messages.success(request, '✅ Registro guardado correctamente.')
        return redirect('planilla')

    claves_numericas = Planilla.objects.filter(clave__regex=r'^\d+$').values_list('clave', flat=True)
    if claves_numericas:
        claves_enteras = [int(k) for k in claves_numericas]
        siguiente_clave = str(max(claves_enteras) + 1)
    else:
        siguiente_clave = '1'

    planteles = Adscripcion.objects.all().order_by('nombre')
    return render(request, 'planilla/altas_nueva.html', {
        'planteles': planteles,
        'siguiente_clave': siguiente_clave
    })

@csrf_exempt
def eliminar_registro(request, no):
    if request.method == 'POST':
        try:
            registro = Planilla.objects.get(no=no)
            registro.delete()
            return JsonResponse({'mensaje': 'Registro eliminado'})
        except Planilla.DoesNotExist:
            return JsonResponse({'error': 'Registro no encontrado'}, status=404)
    return HttpResponseNotAllowed(['POST'])

def consulta(request):
    clave = request.GET.get('clave', '').strip()
    empleado = None

    if clave:
        empleado = Planilla.objects.filter(clave=clave).first()

    if request.method == 'POST' and request.COOKIES.get('autorizacion') != 'lector':
        no = request.POST.get('no')
        empleado = get_object_or_404(Planilla, no=no)
        empleado.nombre = request.POST.get('nombre', empleado.nombre).strip()
        empleado.adscripcion = request.POST.get('adscripcion', empleado.adscripcion).strip()
        empleado.rfc = request.POST.get('rfc', empleado.rfc).strip()
        empleado.curp = request.POST.get('curp', empleado.curp).strip()
        empleado.sindicato = request.POST.get('sindicato', empleado.sindicato).strip()
        empleado.fecha_de_ingreso = request.POST.get('fecha_de_ingreso', empleado.fecha_de_ingreso)
        empleado.save()
        messages.success(request, '✅ Datos actualizados correctamente.')
        return redirect('consulta')

    return render(request, 'planilla/consulta.html', {
        'empleado': empleado,
        'clave_busqueda': clave,
        'autorizacion_usuario': request.COOKIES.get('autorizacion')
    })

def estadisticas(request):
    trabajadores = Planilla.objects.all()
    total_trabajadores = trabajadores.count()
    puestos_unicos = trabajadores.values_list('puesto', flat=True).distinct().count()

    lista_puestos = [
        "COORDINADOR ACADEMICO", "DIRECTOR DE AREA", "DIRECTOR DE PLANTEL A", "DIRECTOR DE PLANTEL B",
        "DIRECTOR GENERAL", "JEFE DE DEPARTAMENTO", "SUBDIRECTOR DE PLANTEL C", "AUXILIAR DE SERVICIOS Y MANTTO",
        "ADMINISTRATIVO ESPECIALIZADO", "ALMACENISTA", "ANALISTA ESPECIALIZADO", "BIBLIOTECARIO", "CAPTURISTA",
        "COOR DE TECNICOS ESPECIALIZADOS", "ENCARGADO DE ORDEN", "ENFERMERA", "INGENIERO EN SISTEMAS",
        "JEFE DE OFICINA", "LABORATORISTA", "OFICIAL DE MANTENIMIENTO", "PROGRAMADOR",
        "SECRETARIA DE DIRECTOR DE AREA", "SECRETARIA DE DIRECTOR DE PLANTEL", "SECRETARIA DE DIRECTOR GENERAL",
        "SUPERVISOR", "TAQUIMECANOGRAFA", "TECNICO ESPECIALIZADO", "TRABAJADORA SOCIAL", "VIGILANTE",
        "OPERADOR DE EQUIPO TIP ESPECIAL", "CHOFER", "DIBUJANTE", "PROF CECYT I",
        "PROF CECYT I (APOYO DOCENCIA) ASOCIADO B MT", "PROF CECYT I (APOYO DOCENCIA) ASOCIADO B TC",
        "PROF CECYT I (APOYO DOCENCIA) ASOCIADO B TT", "PROF CECYT II", "PROF CECYT II (APOYO DOCENCIA) ASOCIADO C MT",
        "PROF CECYT II (APOYO DOCENCIA) ASOCIADO C TC", "PROF CECYT II (APOYO DOCENCIA) ASOCIADO C TT",
        "PROF CECYT III", "PROF CECYT III (APOYO DOCENCIA) ASOCIADO A MT", "PROF CECYT III (APOYO DOCENCIA) ASOCIADO A TC",
        "PROF CECYT III (APOYO DOCENCIA) ASOCIADO A TT", "PROF CECYT IV", "PROF CECYT IV (APOYO DOCENCIA) ASOCIADO B MT",
        "PROF CECYT IV (APOYO DOCENCIA) ASOCIADO B TC", "PROF CECYT IV (APOYO DOCENCIA) ASOCIADO B TT", "TEC DOC CECYT I",
        "TEC DOC CECYT II", "PROF CECYT I ADICIONALES ASOCIADO B", "PROF CECYT II ADICIONALES ASOCIADO C",
        "PROF CECYT III ADICIONALES TITULAR A", "PROF CECYT IV ADICIONALES TITULAR B",
        "TEC DOC CECYT I ADICIONALES TEC DOC ASOC A", "TEC DOC CECYT II ADICIONALES TEC DOC ASOC B",
        "PROF ASOCIADO B MT", "PROF ASOCIADO B TC", "PROF ASOCIADO B TT", "PROF ASOCIADO C MT",
        "PROF ASOCIADO C TC", "PROF ASOCIADO C TT", "PROF TITULAR A MT", "PROF TITULAR A TC",
        "PROF TITULAR A TT", "PROF TITULAR B MT", "PROF TITULAR B TC", "PROF TITULAR B TT",
        "TEC DOC ASOC A MT", "TEC DOC ASOC A TT", "TEC DOC ASOC B TT"
    ]

    puestos_lista = []
    conteo_y_coincidencia = []
    puestos_labels = []
    puestos_data = []
    puestos_sin_ocupar = 0

    for puesto in lista_puestos:
        cantidad_planilla = trabajadores.filter(puesto=puesto).count()
        cantidad_plazas = Plazas.objects.filter(denominacion=puesto).count()
        existe_en_plazas = cantidad_plazas > 0

        if cantidad_planilla > 0:
            puestos_lista.append({'label': puesto, 'cantidad': cantidad_planilla})
            puestos_labels.append(puesto)
            puestos_data.append(cantidad_planilla)
        else:
            puestos_sin_ocupar += 1

        conteo_y_coincidencia.append({
            'puesto': puesto,
            'cantidad_planilla': cantidad_planilla,
            'cantidad_plazas': cantidad_plazas,
            'coincide': existe_en_plazas,
            'diferencia': cantidad_planilla - cantidad_plazas,
        })

    puestos_tuplas = list(zip(puestos_labels, puestos_data))

    context = {
        'total_trabajadores': total_trabajadores,
        'puestos_unicos': puestos_unicos,
        'puestos_sin_ocupar': puestos_sin_ocupar,
        'conteo_y_coincidencia': conteo_y_coincidencia,
        'puestos_lista': puestos_lista,
        'puestos_labels': puestos_labels,
        'puestos_data': puestos_data,
        'puestos_tuplas': puestos_tuplas,
    }

    return render(request, 'planilla/estadisticas.html', context)

def directorio(request):
    directorio = Directorio.objects.all()
    return render(request, 'planilla/directorio.html', {'directorio': directorio})
    
def altas_lista(request):
    # Obtiene la fecha actual
    hoy = timezone.now()
    
    # Filtra por mes y año de ingreso
    altas_mes_actual = Planilla.objects.filter(
        fecha_de_ingreso__year=hoy.year,
        fecha_de_ingreso__month=hoy.month
    ).order_by('-fecha_de_ingreso')

    context = {
        'altas': altas_mes_actual
    }
    return render(request, 'planilla/altas_lista.html', context)


def arbol(request):
    planteles = Planilla.objects.values_list('adscripcion', flat=True).distinct()
    adscripcion = request.GET.get('adscripcion')
    tree_data = {}

    if adscripcion:
        empleados = Planilla.objects.filter(adscripcion=adscripcion)
        director = empleados.filter(puesto__icontains='DIRECTOR DE PLANTEL A').first()
        director_node = {
            "name": f"{director.puesto}\n{director.nombre}" if director else "Sin Director",
            "children": []
        }
        coordinadores = empleados.filter(puesto__icontains='COORDINADOR ACADEMICO')
        for coord in coordinadores:
            director_node["children"].append({
                "name": f"{coord.puesto}\n{coord.nombre}"
            })
        otros = empleados.exclude(puesto__icontains='DIRECTOR DE PLANTEL').exclude(puesto__icontains='COORDINADOR ACADEMICO')
        for otro in otros:
            director_node["children"].append({
                "name": f"{otro.puesto}\n{otro.nombre}"
            })
        tree_data = {
            "name": adscripcion,
            "children": [director_node]
        }
    return render(request, 'planilla/organigrama.html', {
        "planteles": planteles,
        "tree_data": tree_data
    })
