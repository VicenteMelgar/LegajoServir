from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from docxtpl import DocxTemplate
from legajos.models import Legajo, Vinculo
from empleados.models import Empleado
from io import BytesIO
import datetime
import locale

def formulario_reportes(request):
  # Obtener la lista de trabajadores
  empleados = Empleado.objects.all()
  return render(request, 'formulario_reportes.html', {'empleados': empleados})

def generar_constancia(request, id_trabajador):
    trabajador_id = request.GET.get('trabajador')  # ID del trabajador desde el formulario
    trabajador = get_object_or_404(Legajo, id=trabajador_id)  # Buscar el trabajador

    # Filtrar servicios relacionados con el trabajador
    vinculos = Vinculo.objects.filter(legajo__in=[trabajador])  
    
    # Contexto para el template
    context = {
        'empleado': empleado,
        'vinculos': vinculos,
    }

    return render(request, 'constancia_trabajo.html', context)

def descargar_constancia(request, trabajador_id):
    trabajador = get_object_or_404(Legajo, id=trabajador_id)

    # Filtrar servicios prestados seleccionados manualmente
    vinculo_ids = request.GET.getlist('vinculos')
    vinculos = Vinculo.objects.filter(id__in=vinculo_ids, legajo__in=[trabajador])

    # Configurar el idioma a español
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

    # Formatear las fechas en los objetos Vinculo
    for vinculo in vinculos:
        if vinculo.fecha_inicio:
            vinculo.fecha_inicio_formateada = vinculo.fecha_inicio.strftime("%d/%m/%Y")
        else:
            vinculo.fecha_inicio_formateada = ""

        if vinculo.fecha_fin:
            vinculo.fecha_fin_formateada = vinculo.fecha_fin.strftime("%d/%m/%Y")
        else:
            vinculo.fecha_fin_formateada = ""

    # Obtener y formatear la fecha actual
    fecha_actual = datetime.date.today()
    fecha_actual_formateada = fecha_actual.strftime("%d de %B de %Y")

    # Plantilla para constancia
    template_path = 'reportes/plantillas/constancia_template.docx'
    doc = DocxTemplate(template_path)

    context = {
        'nombre': f'{trabajador.empleado.nombres} {trabajador.empleado.apellido_paterno} {trabajador.empleado.apellido_materno}',
        'dni': trabajador.empleado.numero_documento,
        'regimen_laboral': trabajador.get_regimen_laboral_display(),
        'vinculos': vinculos,
        'fecha_actual': fecha_actual_formateada,
    }

    doc.render(context)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = f'attachment; filename="Constancia_{trabajador.empleado.nombres}_{trabajador.empleado.apellido_paterno}_{trabajador.empleado.apellido_materno}.docx"'
    return response

def generar_informe(request, id_empleado):
    empleado_id = request.GET.get('empleado')  # ID del trabajador desde el formulario
    empleado = get_object_or_404(Empleado, id=empleado_id)  # Buscar el trabajador

    # Filtrar servicios relacionados con el trabajador
    vinculos = Vinculo.objects.filter(empleado__in=[empleado])   
    
    # Contexto para el template
    context = {
        'empleado': empleado,
        'vinculos': vinculos,
    }

    return render(request, 'informe_trabajo.html', context)
  
def descargar_informe(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)

    # Filtrar servicios prestados seleccionados manualmente
    vinculo_ids = request.GET.getlist('vinculos')
    vinculos = Vinculo.objects.filter(id__in=vinculo_ids, empleado__in=[empleado])

    # Configurar el idioma a español
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
          
    # Formatear las fechas en los objetos Vinculo
    for vinculo in vinculos:
        if vinculo.resolucion.fecha:
            vinculo.resolucion.fecha_formateada = vinculo.resolucion.fecha.strftime("%d/%m/%Y")
        else:
            vinculo.resolucion.fecha_formateada = ""

    # Obtener y formatear la fecha actual
    fecha_actual = datetime.date.today()
    fecha_actual_formateada = fecha_actual.strftime("%d de %B de %Y")
    
    # Plantilla para informe
    template_path = 'reportes/plantillas/informe_template.docx'
    doc = DocxTemplate(template_path)

    context = {
        'nombre': f'{empleado.nombres} {empleado.apellido_paterno} {empleado.apellido_materno}',
        'dni': empleado.numero_documento,
        'regimen_laboral': empleado.get_regimen_laboral_display(),
        'vinculos': vinculos,
        'fecha_actual': fecha_actual_formateada,
    }

    doc.render(context)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = f'attachment; filename="Informe_{empleado.nombres}_{empleado.apellido_paterno}_{empleado.apellido_materno}.docx"'
    return response

