from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from docxtpl import DocxTemplate
from empleados.models import Empleado, OficinaHistorial, RegimenHistorial, CondicionHistorial, GrupoHistorial, CargoHistorial, NivelHistorial, PlazaHistorial
from legajos.models import Vinculo
from io import BytesIO
import datetime
import locale
from django.contrib.auth.decorators import login_required

@login_required
def formulario_reportes(request):
    # Obtener la lista de empleados
    empleados = Empleado.objects.all().order_by('apellido_paterno')
    return render(request, 'formulario_reportes.html', {'empleados': empleados})

@login_required
def generar_informe(request, id_empleado):
    empleado_id = request.GET.get('empleado')
    empleado = get_object_or_404(Empleado, id=empleado_id)
    
    # Obtener todos los vínculos del empleado
    vinculos = Vinculo.objects.filter(empleado=empleado)
    
    # Obtener información actual del empleado
    oficina_actual = empleado.oficina_actual()
    regimen_actual = empleado.regimen_actual()
    condicion_actual = empleado.condicion_actual()
    grupo_actual = empleado.grupo_actual()
    cargo_actual = empleado.cargo_actual()
    nivel_actual = empleado.nivel_actual()
    plaza_actual = empleado.plaza_actual()

    context = {
        'empleado': empleado,
        'vinculos': vinculos,
        'oficina_actual': oficina_actual,
        'regimen_actual': regimen_actual,
        'condicion_actual': condicion_actual,
        'grupo_actual': grupo_actual,
        'cargo_actual': cargo_actual,
        'nivel_actual': nivel_actual,
        'plaza_actual': plaza_actual,
    }

    return render(request, 'informe_trabajo.html', context)

@login_required  
def descargar_informe(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)

    # Filtrar vínculos seleccionados
    vinculo_ids = request.GET.getlist('vinculos')
    vinculos = Vinculo.objects.filter(id__in=vinculo_ids, empleado=empleado)

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
    
    # Obtener información actual del empleado
    oficina_actual = empleado.oficina_actual()
    regimen_actual = empleado.regimen_actual()
    condicion_actual = empleado.condicion_actual()
    grupo_actual = empleado.grupo_actual()
    cargo_actual = empleado.cargo_actual()
    nivel_actual = empleado.nivel_actual()
    plaza_actual = empleado.plaza_actual()
    
    # Plantilla para informe
    template_path = 'reportes/plantillas/informe_template.docx'
    doc = DocxTemplate(template_path)

    context = {
        'nombre': f'{empleado.nombres} {empleado.apellido_paterno} {empleado.apellido_materno}',
        'dni': empleado.numero_documento,
        'regimen_laboral': regimen_actual.denominacion if regimen_actual else '',
        'oficina_actual': oficina_actual.denominacion if oficina_actual else '',
        'condicion_actual': condicion_actual.denominacion if condicion_actual else '',
        'grupo_actual': grupo_actual.denominacion if grupo_actual else '',
        'cargo_actual': cargo_actual.denominacion if cargo_actual else '',
        'nivel_actual': nivel_actual.denominacion if nivel_actual else '',
        'plaza_actual': plaza_actual.denominacion if plaza_actual else '',
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

@login_required
def generar_constancia(request, id_empleado):
    empleado_id = request.GET.get('empleado')
    empleado = get_object_or_404(Empleado, id=empleado_id)
    
    # Obtener todos los registros históricos
    regimenes = RegimenHistorial.objects.filter(empleado=empleado).order_by('-fecha_inicio')
    oficinas = OficinaHistorial.objects.filter(empleado=empleado).order_by('-fecha_inicio')
    cargos = CargoHistorial.objects.filter(empleado=empleado).order_by('-fecha_inicio')

    context = {
        'empleado': empleado,
        'regimenes': regimenes,
        'oficinas': oficinas,
        'cargos': cargos,
    }

    return render(request, 'constancia_trabajo.html', context)

@login_required
def descargar_constancia(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)

    # Obtener los elementos seleccionados
    regimen_id = request.GET.get('regimen')
    oficina_id = request.GET.get('oficina')
    cargo_id = request.GET.get('cargo')
    plantilla_seleccionada = request.GET.get('plantilla', 'constanciaf')  # Valor por defecto

    # Obtener los objetos seleccionados
    regimen = get_object_or_404(RegimenHistorial, id=regimen_id, empleado=empleado) if regimen_id else None
    oficina = get_object_or_404(OficinaHistorial, id=oficina_id, empleado=empleado) if oficina_id else None
    cargo = get_object_or_404(CargoHistorial, id=cargo_id, empleado=empleado) if cargo_id else None

    # Configurar el idioma a español
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    
    # Formatear fechas en español completo
    def formatear_fecha_completa(fecha):
        if not fecha:
            return "Actualidad"
        try:
            return fecha.strftime("%d de %B de %Y").replace("de de", "de")
        except:
            return fecha.strftime("%d/%m/%Y")

    fecha_inicio_regimen = formatear_fecha_completa(regimen.fecha_inicio) if regimen else ""
    fecha_fin_regimen = formatear_fecha_completa(regimen.fecha_fin) if regimen else "actualidad"

    # Obtener y formatear la fecha actual
    fecha_actual = datetime.date.today()
    fecha_actual_formateada = formatear_fecha_completa(fecha_actual)
    
    # Determinar la plantilla a usar
    plantillas = {
        'constanciaf': 'reportes/plantillas/constanciaf.docx',
        'constanciaf_actual': 'reportes/plantillas/constanciaf_actual.docx',
        'constanciam': 'reportes/plantillas/constanciam.docx',
        'constanciam_actual': 'reportes/plantillas/constanciam_actual.docx',
    }
    
    template_path = plantillas.get(plantilla_seleccionada, plantillas['constanciaf'])

    context = {
        'nombre_completo': f"{empleado.nombres} {empleado.apellido_paterno} {empleado.apellido_materno}",
        'dni': empleado.numero_documento,
        'regimen_laboral': regimen.denominacion if regimen else "",
        'fecha_inicio_regimen': fecha_inicio_regimen,
        'fecha_fin_regimen': fecha_fin_regimen,
        'oficina': oficina.denominacion if oficina else "",
        'cargo': cargo.denominacion if cargo else "",
        'fecha_actual': fecha_actual_formateada,
    }

    doc = DocxTemplate(template_path)
    doc.render(context)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = f'attachment; filename="Constancia_{empleado.apellido_paterno}_{empleado.apellido_materno}.docx"'
    return response