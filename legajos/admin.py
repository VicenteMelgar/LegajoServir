from django.contrib import admin
from django.utils.html import format_html
from .models import Legajo, Vinculo, DocumentoLegajo, Compensacion, Movimiento, Formacion, Experiencia

@admin.register(Legajo)
class LegajoAdmin(admin.ModelAdmin):
  list_display = ('empleado_apellido_paterno', 'empleado_apellido_materno', 'empleado_nombres', 'empleado_numero_documento', 'regimen_laboral', 'activo')
  search_fields = ('empleado__apellido_paterno', 'empleado__apellido_materno', 'empleado__nombres', 'empleado__numero_documento', 'regimen_laboral')

  def empleado_apellido_paterno(self, obj):
    return obj.empleado.apellido_paterno
  empleado_apellido_paterno.short_description = 'Apellido Paterno'

  def empleado_apellido_materno(self, obj):
    return obj.empleado.apellido_materno
  empleado_apellido_materno.short_description = 'Apellido Materno'

  def empleado_nombres(self, obj):
    return obj.empleado.nombres
  empleado_nombres.short_description = 'Nombres'

  def empleado_numero_documento(self, obj):
    return obj.empleado.numero_documento
  empleado_numero_documento.short_description = 'DNI'
    
@admin.register(Vinculo)
class VinculoAdmin(admin.ModelAdmin):
  list_display = ('empleado', 'tipo', 'resolucion', 'descripcion', 'ver_resolucion_pdf')
  search_fields = ('empleado',)
  autocomplete_fields = ['legajos']

  def legajos(self, obj):
    return ", ".join([str(l) for l in obj.legajos.all()])

  def ver_resolucion_pdf(self, obj):
    if obj.resolucion and obj.resolucion.pdf:
      return format_html('<a href="{}" target="_blank">Documento</a>', obj.resolucion.pdf.url)
    return "No disponible"

  ver_resolucion_pdf.short_description = "Visualizar PDF"

@admin.register(DocumentoLegajo)
class DocumentoLegajoAdmin(admin.ModelAdmin):
  list_display = ('empleado', 'categoria', 'documento', 'descripcion', 'fecha', 'ver_pdf')
  search_fields = ('empleado', 'categoria', 'descripcion')
  autocomplete_fields = ['legajos']

  def legajos(self, obj):
    return ", ".join([str(l) for l in obj.legajos.all()])

@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):
  list_display = ('empleado', 'resolucion', 'motivo', 'asunto', 'desde', 'hasta', 'total_dias', 'ver_resolucion_pdf')
  list_filter = ('empleado', 'resolucion')
  search_fields = ('empleado', 'asunto')
  autocomplete_fields = ['legajos']

  def legajos(self, obj):
    return ", ".join([str(l) for l in obj.legajos.all()])

  def ver_resolucion_pdf(self, obj):
    if obj.resolucion and obj.resolucion.pdf:
      return format_html('<a href="{}" target="_blank">Documento</a>', obj.resolucion.pdf.url)
    return "No disponible"

  ver_resolucion_pdf.short_description = "Visualizar PDF"

@admin.register(Formacion)
class FormacionAdmin(admin.ModelAdmin):
  list_display = ('empleado', 'formacion', 'documento', 'fecha', 'ver_pdf')
  list_filter = ('formacion',)
  search_fields = ('formacion',)
  autocomplete_fields = ['legajos']

  def legajos(self, obj):
    return ", ".join([str(l) for l in obj.legajos.all()])

@admin.register(Compensacion)
class CompensacionAdmin(admin.ModelAdmin):
  list_display = ('resolucion', 'motivo', 'descripcion', 'fecha', 'ver_resolucion_pdf')
  list_filter = ('resolucion',)
  search_fields = ('resolucion__numero',)
  autocomplete_fields = ['legajos']

  def legajos(self, obj):
    return ", ".join([str(l) for l in obj.legajos.all()])

  def ver_resolucion_pdf(self, obj):
    if obj.resolucion and obj.resolucion.pdf:
      return format_html('<a href="{}" target="_blank">Documento</a>', obj.resolucion.pdf.url)
    return "No disponible"

  ver_resolucion_pdf.short_description = "Visualizar PDF"

@admin.register(Experiencia)
class ExperienciaAdmin(admin.ModelAdmin):
  list_display = ('institucion', 'documento', 'numero', 'cargo', 'fecha_inicio', 'fecha_fin', 'fecha_expedicion', 'ver_pdf')
  list_filter = ('institucion', 'documento')
  search_fields = ('institucion', 'documento')
  autocomplete_fields = ['legajos']

  def legajos(self, obj):
    return ", ".join([str(l) for l in obj.legajos.all()])