from django.db import models
from documentos.models import Resolucion
from .choices import estados, sexo, departamento, documento_identidad, condicion_laboral, departamento_oficina, regimen_laboral, grupo_ocupacional, cargos, niveles
              
# Modelo para agregar empleado
class Empleado(models.Model):
    apellido_paterno = models.CharField(max_length=50)
    apellido_materno = models.CharField(max_length=50)
    nombres = models.CharField(max_length=50)
    documento_identidad = models.CharField(max_length=100, choices=documento_identidad)
    numero_documento = models.CharField(max_length=15, unique=True)
    sexo = models.CharField(max_length=1, choices= sexo, blank=True, null=True)
    estado_civil = models.CharField(max_length=10, choices= estados, blank=True, null=True)
    telefono = models.CharField(max_length=12, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    departamento = models.CharField(max_length=50, choices= departamento, blank=True, null=True)
    provincia = models.CharField(max_length=50, blank=True, null=True)
    distrito = models.CharField(max_length=50, blank=True, null=True)
    domicilio = models.CharField(max_length=100, blank=True, null=True)
    
    def oficina_actual(self):
        return self.oficinahistorial_set.filter(fecha_fin__isnull=True).order_by('-fecha_inicio').first()

    def regimen_actual(self):
        return self.regimenhistorial_set.filter(fecha_fin__isnull=True).order_by('-fecha_inicio').first()
      
    def condicion_actual(self):
        return self.condicionhistorial_set.filter(fecha_fin__isnull=True).order_by('-fecha_inicio').first()

    def grupo_actual(self):
        return self.grupohistorial_set.filter(fecha_fin__isnull=True).order_by('-fecha_inicio').first()

    def cargo_actual(self):
        return self.cargohistorial_set.filter(fecha_fin__isnull=True).order_by('-fecha_inicio').first()

    def nivel_actual(self):
        return self.nivelhistorial_set.filter(fecha_fin__isnull=True).order_by('-fecha_inicio').first()

    def plaza_actual(self):
        return self.plazahistorial_set.filter(fecha_fin__isnull=True).order_by('-fecha_inicio').first()

    def __str__(self):
        return f"{self.apellido_paterno} {self.apellido_materno}, {self.nombres}"
    
    class Meta:
        ordering = ['apellido_paterno']
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'

# Modelo de oficina
class OficinaHistorial(models.Model):
  empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
  resolucion = models.ForeignKey(Resolucion, on_delete=models.CASCADE, verbose_name='Resolución')
  denominacion = models.CharField(max_length=100, choices=departamento_oficina, verbose_name='Departamento u Oficina')
  fecha_inicio = models.DateField(null=True, blank=True, verbose_name="Fecha de Inicio")
  fecha_fin = models.DateField(blank=True, null=True, verbose_name='Fecha de Finalización')

  def __str__(self):
      return self.denominacion
  
  class Meta:
    ordering = ['-fecha_inicio']
    verbose_name = 'Departamento u Oficina'
    verbose_name_plural = 'Departamentos u Oficinas'
    
# Modelo de Régimen Laboral
class RegimenHistorial(models.Model):
  empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
  resolucion = models.ForeignKey(Resolucion, on_delete=models.CASCADE, verbose_name='Resolución')
  denominacion = models.CharField(max_length=100, choices=regimen_laboral, verbose_name='Régimen Laboral')
  fecha_inicio = models.DateField(null=True, blank=True, verbose_name="Fecha de Inicio")
  fecha_fin = models.DateField(blank=True, null=True, verbose_name='Fecha de Finalización')

  def __str__(self):
      return self.denominacion
  
  class Meta:
    ordering = ['-fecha_inicio']
    verbose_name = 'Régimen Laboral'
    verbose_name_plural = 'Régimen Laboral'
    
# Modelo de Condición Laboral 
class CondicionHistorial(models.Model):
  empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
  resolucion = models.ForeignKey(Resolucion, on_delete=models.CASCADE, verbose_name='Resolución')
  denominacion = models.CharField(max_length=100, choices= condicion_laboral, verbose_name='Denominación')
  fecha_inicio = models.DateField(null=True, blank=True, verbose_name="Fecha de Inicio")
  fecha_fin = models.DateField(blank=True, null=True, verbose_name='Fecha de Finalización')

  def __str__(self):
      return self.denominacion
  
  class Meta:
    ordering = ['-fecha_inicio']
    verbose_name = 'Condición Laboral'
    verbose_name_plural = 'Condición Laboral'

# Modelo de Grupo Ocupacional
class GrupoHistorial(models.Model):
  empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
  resolucion = models.ForeignKey(Resolucion, on_delete=models.CASCADE, verbose_name='Resolución')
  denominacion = models.CharField(max_length=100, choices= grupo_ocupacional, verbose_name='Denominación')
  fecha_inicio = models.DateField(null=True, blank=True, verbose_name="Fecha de Inicio")
  fecha_fin = models.DateField(blank=True, null=True, verbose_name='Fecha de Finalización')

  def __str__(self):
      return self.denominacion
  
  class Meta:
    ordering = ['-fecha_inicio']
    verbose_name = 'Grupo Ocupacional'
    verbose_name_plural = 'Grupos Ocupacionales'
    
# Modelo de Cargo
class CargoHistorial(models.Model):
  empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
  resolucion = models.ForeignKey(Resolucion, on_delete=models.CASCADE, verbose_name='Resolución')
  denominacion = models.CharField(max_length=100, choices= cargos, verbose_name='Cargo')
  fecha_inicio = models.DateField(null=True, blank=True, verbose_name="Fecha de Inicio")
  fecha_fin = models.DateField(blank=True, null=True, verbose_name='Fecha de Finalización')

  def __str__(self):
      return self.denominacion
  
  class Meta:
    ordering = ['-fecha_inicio']
    verbose_name = 'Cargo'
    verbose_name_plural = 'Cargos'
    
# Modelo de Nivel
class NivelHistorial(models.Model):
  empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
  resolucion = models.ForeignKey(Resolucion, on_delete=models.CASCADE, verbose_name='Resolución')
  denominacion = models.CharField(max_length=100, choices= niveles, verbose_name='Denominación')
  fecha_inicio = models.DateField(null=True, blank=True, verbose_name="Fecha de Inicio")
  fecha_fin = models.DateField(blank=True, null=True, verbose_name='Fecha de Finalización')

  def __str__(self):
      return self.denominacion
  
  class Meta:
    ordering = ['-fecha_inicio']
    verbose_name = 'Nivel'
    verbose_name_plural = 'Niveles'

# Modelo de Plaza
class PlazaHistorial(models.Model):
  empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
  resolucion = models.ForeignKey(Resolucion, on_delete=models.CASCADE, verbose_name='Resolución')
  denominacion = models.CharField(max_length=100, verbose_name='Número de Plaza (airhsp)')
  fecha_inicio = models.DateField(null=True, blank=True, verbose_name="Fecha de Inicio")
  fecha_fin = models.DateField(blank=True, null=True, verbose_name='Fecha de Finalización')

  def __str__(self):
      return self.denominacion
  
  class Meta:
    ordering = ['-fecha_inicio']
    verbose_name = 'Plaza (airhsp)'
    verbose_name_plural = 'Plaza (airhsp)'
