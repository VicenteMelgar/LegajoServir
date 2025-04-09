from django.db import models
from empleados.models import Empleado
from documentos.models import Resolucion
from django.utils.html import format_html
from .choices import categorias, tipo_formacion, tipo_historial, documentos_experiencia, tipo_movimientos, documentos_regimen
from django.core.exceptions import ValidationError

# Modelo para Aperturar Legajos
class Legajo(models.Model):
  empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='legajos')
  regimen_laboral = models.CharField(max_length=100, choices=documentos_regimen, verbose_name='Régimen Laboral')
  fecha_creacion = models.DateField(auto_now_add=True)
  activo = models.BooleanField(default=True)  # Para marcar el legajo actual

  def __str__(self):
    return f"{self.empleado.apellido_paterno} {self.empleado.apellido_materno}, {self.empleado.nombres} - {self.regimen_laboral}"

  def clean(self):
    super().clean()
    if self.id is None: # Si es un legajo nuevo
      if Legajo.objects.filter(empleado=self.empleado, regimen_laboral=self.regimen_laboral).exists():
        raise ValidationError(f"El empleado ya tiene un legajo de tipo {self.regimen_laboral}.")
    else: # Si es un legajo existente que se está modificando
      if Legajo.objects.filter(empleado=self.empleado, regimen_laboral=self.regimen_laboral).exclude(id=self.id).exists():
        raise ValidationError(f"El empleado ya tiene un legajo de tipo {self.regimen_laboral}.")

  def save(self, *args, **kwargs):
    self.full_clean()
    super(Legajo, self).save(*args, **kwargs)

    if self.activo:
      # Desactiva los otros legajos del mismo empleado
      Legajo.objects.filter(empleado=self.empleado).exclude(id=self.id).update(activo=False)
            
# Modelo de Vinculo laboral
class Vinculo(models.Model):
  empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
  legajos = models.ManyToManyField('Legajo', related_name='vinculos_legajo')
  tipo = models.CharField(max_length=100, choices=tipo_historial)
  resolucion = models.ForeignKey(Resolucion, on_delete=models.CASCADE, verbose_name='Resolución')
  descripcion = models.CharField(max_length=1000, blank=True, verbose_name='Descripción')
  
  def __str__(self):
    return self.descripcion
  
  class Meta:
    ordering = ['-resolucion__fecha']
    verbose_name = 'Historial Laboral'
    verbose_name_plural = 'Historial Laboral'
 
# Compensaciones
class Compensacion(models.Model):
  empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
  legajos = models.ManyToManyField('Legajo', related_name='compensaciones_legajo')
  resolucion = models.ForeignKey(Resolucion, on_delete=models.CASCADE, verbose_name='Resolución')
  motivo = models.CharField(max_length=50)
  descripcion = models.CharField(max_length=250, blank=True)
  fecha = models.DateField()
  
  def __str__(self):
    return self.descripcion
  
  class Meta:
    verbose_name = 'Compensación'
    verbose_name_plural = 'Compensaciones'
    
# Movimientos del Personal
class Movimiento(models.Model):
  empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
  legajos = models.ManyToManyField('Legajo', related_name='movimientos_legajo')
  resolucion = models.ForeignKey(Resolucion, on_delete=models.CASCADE, verbose_name='Resolución')
  tipo = models.CharField(max_length=100, choices=tipo_movimientos, blank=True, null=True, verbose_name='Tipo de Licencia')
  motivo = models.CharField(max_length=50)
  asunto = models.CharField(max_length=50)
  desde = models.DateField(blank=True, null=True)
  hasta = models.DateField(blank=True, null=True)
  total_dias = models.PositiveIntegerField(blank=True, null=True, verbose_name='Total de Días')

  def save(self, *args, **kwargs):
      if self.desde and self.hasta:
          diferencia = self.hasta - self.desde
          self.total_dias = diferencia.days + 1  # Sumamos 1 para incluir el día de inicio
      elif self.desde and not self.hasta:
          self.total_dias = 1
      else:
          self.total_dias = 0
      super(Movimiento, self).save(*args, **kwargs)
  
  def __str__(self):
    return self.asunto

  class Meta:
    ordering = ['-desde']
    verbose_name = 'Movimiento del Personal'
    verbose_name_plural = 'Movimientos del Personal'

# Modelo de DocumentoLegajo
class DocumentoLegajo(models.Model):
  empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
  legajos = models.ManyToManyField('Legajo', related_name='documentos_legajo')
  categoria = models.CharField(max_length=50, choices=categorias)
  documento = models.CharField(max_length=100, verbose_name='Tipo de Documento')
  numero = models.CharField(max_length=50, blank=True, null=True, verbose_name='Número')
  descripcion = models.CharField(max_length=1000, blank=True, null=True)
  fecha = models.DateField(blank=True, null=True, verbose_name='Fecha del Documento')
  fecha_inicio = models.DateField(blank=True, null=True, verbose_name='Fecha de Inicio')
  fecha_fin = models.DateField(blank=True, null=True, verbose_name='Fecha de Finalización')
  total_dias = models.PositiveIntegerField(blank=True, null=True, verbose_name='Total de Días')
  puntaje = models.PositiveSmallIntegerField(blank=True, null=True)
  pdf = models.FileField(upload_to='documentos_legajo/', verbose_name='Cargar PDF', blank=True, null=True)

  def ver_pdf(self):
      if self.pdf:
          return format_html('<a href="{}" target="_blank">Documento</a>', self.pdf.url)
      return "No disponible"
  
  ver_pdf.short_description = "Visualizar PDF"
  
  def __str__(self):
    return f'{self.categoria}, {self.documento}'
  
  class Meta:
    ordering = ['descripcion']
    verbose_name = 'Documento Legajo'
    verbose_name_plural = 'Documentos Legajos'
    
class Formacion(models.Model):
  empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
  legajos = models.ManyToManyField('Legajo', related_name='formaciones_legajo')
  formacion = models.CharField(max_length=50, choices=tipo_formacion)
  centro = models.CharField(max_length=250, blank=True, null=True, verbose_name='Institución')
  documento = models.CharField(max_length=100, blank=True, null=True)
  descripcion = models.CharField(max_length=250, blank=True, null=True)
  mencion = models.CharField(max_length=100, blank=True, null=True)
  especialidad = models.CharField(max_length=100, blank=True, null=True)
  subespecialidad = models.CharField(max_length=100, blank=True, null=True)
  cod_especialidad = models.CharField(max_length=50, blank=True, null=True)
  colegiatura = models.CharField(max_length=25, blank=True, null=True)
  fecha = models.DateField(blank=True, null=True)
  fecha_inicio = models.DateField(blank=True, null=True)
  fecha_fin = models.DateField(blank=True, null=True)
  fecha_vigencia = models.DateField(blank=True, null=True)
  horas = models.PositiveSmallIntegerField(blank=True, null=True)
  creditos = models.PositiveSmallIntegerField(blank=True, null=True)
  pdf = models.FileField(upload_to='documentos_formacion/', verbose_name='Cargar PDF', blank=True, null=True)
 
  def ver_pdf(self):
    if self.pdf:
      return format_html('<a href="{}" target="_blank">Ver PDF</a>', self.pdf.url)
    return "No disponible"
  
  ver_pdf.short_description = "Visualizar PDF"
  
  def __str__(self):
    return self.formacion
  
  class Meta:
    ordering = ['-fecha']
    verbose_name = 'Formación Académica'
    verbose_name_plural = 'Formación Académica'

# Experiencia Laboral
class Experiencia(models.Model):
  empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
  legajos = models.ManyToManyField('Legajo', related_name='experiencias_legajo')
  institucion = models.CharField(max_length=250, null=True, blank=True, verbose_name='Institución o Empresa')
  documento = models.CharField(max_length=100, blank=True, null=True, choices=documentos_experiencia, verbose_name='Tipo de Documento')
  numero = models.CharField(blank=True, null=True, max_length=50, unique=True, verbose_name='Número')
  cargo = models.CharField(max_length=250,)
  fecha_inicio = models.DateField()
  fecha_fin = models.DateField()
  fecha_expedicion = models.DateField(blank=True, null=True)
  pdf = models.FileField(upload_to='experiencia_laboral/', verbose_name='Cargar PDF', blank=True, null=True)

  def ver_pdf(self):
    if self.pdf:
      return format_html('<a href="{}" target="_blank">Ver PDF</a>', self.pdf.url)
    return "No disponible"
  
  ver_pdf.short_description = "Visualizar PDF"
  
  def __str__(self):
    return self.institucion
  
  class Meta:
    ordering = ['-fecha_inicio']
    verbose_name = 'Experiencia Laboral'
    verbose_name_plural = 'Experiencia Laboral'

