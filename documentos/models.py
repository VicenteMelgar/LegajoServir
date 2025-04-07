from django.db import models
from django.utils.html import format_html
from .choices import documento

# Modelo de Resolución
class Resolucion(models.Model):
  documento = models.CharField(max_length=100, choices= documento, blank=True, null=True)
  numero = models.CharField(max_length=50, unique=True, verbose_name='Número de Resolución')
  fecha = models.DateField(verbose_name="Fecha del Documento")
  pdf = models.FileField(upload_to='resoluciones/', verbose_name='Cargar PDF', blank=True, null=True)

  def ver_pdf(self):
      if self.pdf:
          return format_html('<a href="{}" target="_blank">Documento</a>', self.pdf.url)
      return "No disponible"
  
  ver_pdf.short_description = "Visualizar PDF"

  def __str__(self):
      return f'{self.documento} Nº {self.numero}'
  
  class Meta:
    ordering = ['-fecha']
    verbose_name = 'Resolución'
    verbose_name_plural = 'Resoluciones'