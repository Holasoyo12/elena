from django.shortcuts import render
from .models import Alumnos
from .forms import ComentarioContactoForm
from .models import Comentario
from .models import ComentarioContacto
from .models import Archivos
from .forms import FormArchivos
from django.contrib import messages
from django.shortcuts import get_object_or_404
import datetime

# ---------------------------------------
# VISTA PRINCIPAL
# ---------------------------------------
def registros(request):
    alumnos = Alumnos.objects.all()
    return render(request, 'registros/principal.html', {'alumnos': alumnos})


# ---------------------------------------
# COMENTARIOS CONTACTO
# ---------------------------------------
def comentarios(request):
    comentarios = ComentarioContacto.objects.all()
    return render(request, 'registros/Comentarios.html', {'comentarios': comentarios})


def registrar(request):
    if request.method == 'POST':
        form = ComentarioContactoForm(request.POST)
        if form.is_valid():
            form.save()
            comentarios = ComentarioContacto.objects.all()
            return render(request, 'registros/Comentarios.html', {'comentarios': comentarios})

    form = ComentarioContactoForm()
    return render(request, 'registros/contacto.html', {'form': form})


def contacto(request):
    return render(request, "registros/contacto.html")

def consultaComentarioContacto(request):
    comentarios = ComentarioContacto.objects.all()
    return render(request, 'registros/consultaContacto.html', {'comentarios': comentarios})

def eliminarComentarioContacto(request, id,
    confirmacion = 'registros/confirmarEliminar.html'):
    comentario = get_object_or_404(ComentarioContacto, id=id)
    if request.method == 'POST':
        comentario.delete()
        comentarios = ComentarioContacto.objects.all()
        return render(request, 'registros/consultaContacto.html', {'comentarios': comentarios})
    
    return render(request, confirmacion, {'comentario': comentario})

def consultarComentarioIndividual(request, id):
    comentario=ComentarioContacto.objects.get(id=id)

    return render(request, 'registros/fromEditarComentario.html', {'comentario': comentario})

def editarComentarioContacto(request, id):
    comentario = get_object_or_404(ComentarioContacto, id=id)
    form = ComentarioContactoForm(request.POST, instance=comentario)

    if form.is_valid():
        form.save()
        comentarios = ComentarioContacto.objects.all()
        return render(request, 'registros/consultaContacto.html', {'comentarios': comentarios})
    
    return render(request, 'registros/fromEditarComentario.html', {'comentario': comentario})


# ---------------------------------------
# CONSULTAS ALUMNOS
# ---------------------------------------
def consultar1(request):
    alumnos = Alumnos.objects.filter(carrera="TI")
    return render(request, 'registros/consultas.html', {'alumnos': alumnos})


def consultar2(request):
    alumnos = Alumnos.objects.filter(carrera="TI", turno="Matutino")
    return render(request, 'registros/consultas.html', {'alumnos': alumnos})


def consultar3(request):
    alumnos = Alumnos.objects.all().only("matricula", "nombre", "carrera", "turno", "imagen")
    return render(request, 'registros/consultas.html', {'alumnos': alumnos})


def consultar4(request):
    alumnos = Alumnos.objects.filter(turno__contains="Vesp")
    return render(request, 'registros/consultas.html', {'alumnos': alumnos})


def consultar5(request):
    alumnos = Alumnos.objects.filter(nombre__in=["Juan", "Ana"])
    return render(request, 'registros/consultas.html', {'alumnos': alumnos})


def consulta6(request):
    fechaInicio = datetime.date(2025, 11, 1)
    fechaFin = datetime.date(2025, 11, 30)
    alumnos = Alumnos.objects.filter(created__range=(fechaInicio, fechaFin))
    return render(request, 'registros/consultas.html', {'alumnos': alumnos})


def consulta7(request):
    alumnos = Alumnos.objects.filter(comentario__coment__contains='No inscrito')
    return render(request, 'registros/consultas.html', {'alumnos': alumnos})


# ---------------------------------------
# CONSULTAS DE LA ACTIVIDAD (MODELO Comentario)
# ---------------------------------------

def consulta_comentarios_rango(request):
    fecha_inicio = datetime.date(2024, 11, 20)
    fecha_fin = datetime.date(2024, 11, 26)

    comentarios = Comentario.objects.filter(created__range=(fecha_inicio, fecha_fin))

    return render(request, "registros/consultas_comentarios.html", {
        'titulo': 'Comentarios entre el 20 y 26 de noviembre',
        'comentarios': comentarios
    })


def consulta_buscar_expresion(request):
    comentarios = Comentario.objects.filter(comentario__icontains="ejemplo")
    return render(request, "registros/consultas_comentarios.html", {
        'titulo': 'Buscar expresión en comentario',
        'comentarios': comentarios
    })


def consulta_por_usuario(request):
    comentarios = Comentario.objects.filter(usuario__username="Marco")
    return render(request, "registros/consultas_comentarios.html", {
        'titulo': 'Comentarios de un usuario',
        'comentarios': comentarios
    })


def consulta_solo_comentarios(request):
    solo = Comentario.objects.values_list("comentario", flat=True)
    return render(request, "registros/consultas_comentarios.html", {
        'titulo': 'Solo los textos de comentarios',
        'solo_comentarios': solo
    })


def consulta_expresion_extra(request):
    comentarios = Comentario.objects.filter(comentario__startswith="Hola")
    return render(request, "registros/consultas_comentarios.html", {
        'titulo': 'Comentarios que empiezan con "Hola"',
        'comentarios': comentarios
    })

def archivos(request):
    if request.method == 'POST':
        form = FormArchivos(request.POST, request.FILES)
        if form.is_valid():
            titulo = request.POST['titulo']
            descripcion = request.POST['descripcion']
            archivo = request.FILES['archivo']
            insert = Archivos(titulo=titulo, descripcion=descripcion,
            archivo=archivo)
            insert.save()
            return render(request,"registros/archivos.html")
        else:
            messages.error(request, "Error al procesar el formulario")
    else:
        return render(request,"registros/archivos.html",{'archivo':Archivos})
    
def consultasSQL(request):
    alumnos=Alumnos.objects.raw('SELECT id, matricula, nombre, carrera, turno, imagen from registros_alumnos WHERE carrera="TI" ORDER BY turno DESC')
    return render(request,"registros/consultas.html",{'alumnos':alumnos})