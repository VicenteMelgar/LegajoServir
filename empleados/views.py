from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Empleado, OficinaHistorial, RegimenHistorial, CondicionHistorial, GrupoHistorial, CargoHistorial, NivelHistorial, PlazaHistorial
from django.contrib.auth.decorators import login_required

@login_required   
def datospersonales_lista(request):
  query = request.GET.get('searchorders', '')  # Texto ingresado en el buscador
  filters = Q(apellido_paterno__icontains=query) | Q(apellido_materno__icontains=query) | Q(nombres__icontains=query)

  empleados = Empleado.objects.filter(filters)

  # Construir una lista de empleados con su información vigente
  empleados_con_datos = []
  for emp in empleados:
    empleados_con_datos.append({
      'empleado': emp,
      'oficina_actual': emp.oficina_actual(),
      'regimen_actual': emp.regimen_actual(),
      'condicion_actual': emp.condicion_actual(),
      'grupo_actual': emp.grupo_actual(),
      'cargo_actual': emp.cargo_actual(),
      'nivel_actual': emp.nivel_actual(),
      'plaza_actual': emp.plaza_actual(),
    })

  # Preparar contexto
  context = {
    'empleados': empleados_con_datos,
    'query': query  # Para mantener el texto en el campo de búsqueda
  }

  return render(request, 'empleados.html', context)

@login_required   
# Vista para actualizar Historial Laboral Personal
def info_historial(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)
    
    # Obtener registros históricos
    oficina_historial = OficinaHistorial.objects.filter(empleado=empleado).order_by('-fecha_inicio')
    regimen_historial = RegimenHistorial.objects.filter(empleado=empleado).order_by('-fecha_inicio')
    condicion_historial = CondicionHistorial.objects.filter(empleado=empleado).order_by('-fecha_inicio')
    grupo_historial = GrupoHistorial.objects.filter(empleado=empleado).order_by('-fecha_inicio')
    cargo_historial = CargoHistorial.objects.filter(empleado=empleado).order_by('-fecha_inicio')
    nivel_historial = NivelHistorial.objects.filter(empleado=empleado).order_by('-fecha_inicio')
    plaza_historial = PlazaHistorial.objects.filter(empleado=empleado).order_by('-fecha_inicio')

    return render(request, 'info_historial.html', {
        'empleado': empleado,
        'oficina_historial': oficina_historial,
        'regimen_historial': regimen_historial,
        'condicion_historial': condicion_historial,
        'grupo_historial': grupo_historial,
        'cargo_historial': cargo_historial,
        'nivel_historial': nivel_historial,
        'plaza_historial': plaza_historial
    })

