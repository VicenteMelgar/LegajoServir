from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from empleados.models import Empleado 
from documentos.models import Resolucion
from .models import Vinculo, Experiencia, Formacion, Movimiento, Compensacion, DocumentoLegajo, Legajo
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('legajos:dashboard') 
 
@login_required   
def legajos_lista(request):
  query = request.GET.get('buscar', '')  # Obtén el texto ingresado en el buscador
  filters = Q(regimen_laboral__icontains=query) | Q(empleado__apellido_paterno__icontains=query) | Q(empleado__apellido_materno__icontains=query) | Q(empleado__nombres__icontains=query)
  
  legajos = Legajo.objects.filter(filters)  # Obtén todos los legajos
  context = {
      'legajos': legajos,
      'query': query  # Para mantener el texto en el campo de búsqueda
  }
  return render(request, 'legajos_lista.html', context)

@login_required
def documentos(request):
    query = request.GET.get('buscador', '')
    filters = Q(documento__icontains=query) | Q(numero__icontains=query)

    todos_documentos = Resolucion.objects.filter(filters)
    context = {
        'todos_documentos': todos_documentos,
        'query': query
    }
    return render(request, 'documentos.html', context)

@login_required
def info_general(request, legajo_id):
    legajo = get_object_or_404(Legajo.objects.select_related('empleado'), id=legajo_id)
    empleado = legajo.empleado

    # Utilidades para filtrar por legajo asociado
    def filtrar_por_legajo(queryset, tipo=None, categoria=None):
        qs = queryset.filter(legajos=legajo)
        if tipo:
            qs = qs.filter(tipo=tipo)
        if categoria:
            qs = qs.filter(categoria=categoria)
        return qs

    context = {
        'legajo': legajo,

        # Vínculos
        'incorporacion': filtrar_por_legajo(empleado.vinculo_set, tipo='Incorporación'),
        'progresion': filtrar_por_legajo(empleado.vinculo_set, tipo='Progresión'),
        'desplazamiento': filtrar_por_legajo(empleado.vinculo_set, tipo='Desplazamiento'),
        'desvinculacion': filtrar_por_legajo(empleado.vinculo_set, tipo='Desvinculación'),

        # Experiencia, formación, etc.
        'experiencias': filtrar_por_legajo(empleado.experiencia_set),
        'formaciones': filtrar_por_legajo(empleado.formacion_set),
        'movimientos': filtrar_por_legajo(empleado.movimiento_set),
        'compensaciones': filtrar_por_legajo(empleado.compensacion_set),

        # Documentos por categoría
        'info_personal': filtrar_por_legajo(empleado.documentolegajo_set, categoria='informacion_personal'),
        'incorporacion_docs': filtrar_por_legajo(empleado.documentolegajo_set, categoria='incorporacion'),
        'evaluacion': filtrar_por_legajo(empleado.documentolegajo_set, categoria='evaluacion'),
        'reconocimiento': filtrar_por_legajo(empleado.documentolegajo_set, categoria='reconocimiento'),
        'laboral': filtrar_por_legajo(empleado.documentolegajo_set, categoria='laboral'),
        'seguridad': filtrar_por_legajo(empleado.documentolegajo_set, categoria='seguridad'),
        'desvinculacion_docs': filtrar_por_legajo(empleado.documentolegajo_set, categoria='desvinculacion'),
        'otro': filtrar_por_legajo(empleado.documentolegajo_set, categoria='otro'),
    }

    return render(request, 'info_general.html', context)

# Vista para dashboard
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')