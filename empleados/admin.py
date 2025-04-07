from django.contrib import admin
from .models import (
    Empleado,
    OficinaHistorial,
    RegimenHistorial,
    CondicionHistorial,
    GrupoHistorial,
    CargoHistorial,
    NivelHistorial,
    PlazaHistorial,
)

admin.site.site_header = "DASHBOARD LEGAJO"
admin.site.site_title = "Panel de Administración"
admin.site.index_title = "Bienvenido al Sistema de Administración"
 
@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('apellido_paterno', 'apellido_materno', 'nombres', 'numero_documento', 'email')
    search_fields = ('apellido_paterno', 'apellido_materno', 'nombres', 'numero_documento')

@admin.register(OficinaHistorial)
class OficinaHistorialAdmin(admin.ModelAdmin):
    list_display = ('empleado_numero_documento', 'empleado_apellido_paterno', 'empleado_apellido_materno', 'empleado_nombres', 'denominacion', 'fecha_inicio', 'fecha_fin')
    search_fields = ('empleado__numero_documento', 'empleado__apellido_paterno', 'empleado__apellido_materno', 'empleado__nombres')
    
    def empleado_numero_documento(self, obj):
        return obj.empleado.numero_documento
    empleado_numero_documento.short_description = 'DNI'
    
    def empleado_apellido_paterno(self, obj):
        return obj.empleado.apellido_paterno
    empleado_apellido_paterno.short_description = 'Apellido Paterno'

    def empleado_apellido_materno(self, obj):
        return obj.empleado.apellido_materno
    empleado_apellido_materno.short_description = 'Apellido Materno'

    def empleado_nombres(self, obj):
        return obj.empleado.nombres
    empleado_nombres.short_description = 'Nombres'

@admin.register(RegimenHistorial)
class RegimenHistorialAdmin(admin.ModelAdmin):
    list_display = ('empleado_numero_documento', 'empleado_apellido_paterno', 'empleado_apellido_materno', 'empleado_nombres', 'denominacion', 'fecha_inicio', 'fecha_fin')
    search_fields = ('empleado__numero_documento', 'empleado__apellido_paterno', 'empleado__apellido_materno', 'empleado__nombres')
    
    def empleado_numero_documento(self, obj):
        return obj.empleado.numero_documento
    empleado_numero_documento.short_description = 'DNI'
    
    def empleado_apellido_paterno(self, obj):
        return obj.empleado.apellido_paterno
    empleado_apellido_paterno.short_description = 'Apellido Paterno'

    def empleado_apellido_materno(self, obj):
        return obj.empleado.apellido_materno
    empleado_apellido_materno.short_description = 'Apellido Materno'

    def empleado_nombres(self, obj):
        return obj.empleado.nombres
    empleado_nombres.short_description = 'Nombres'
    
@admin.register(CondicionHistorial)
class CondicionHistorialAdmin(admin.ModelAdmin):
    list_display = ('empleado_numero_documento', 'empleado_apellido_paterno', 'empleado_apellido_materno', 'empleado_nombres', 'denominacion', 'fecha_inicio', 'fecha_fin')
    search_fields = ('empleado__numero_documento', 'empleado__apellido_paterno', 'empleado__apellido_materno', 'empleado__nombres')
    
    def empleado_numero_documento(self, obj):
        return obj.empleado.numero_documento
    empleado_numero_documento.short_description = 'DNI'
    
    def empleado_apellido_paterno(self, obj):
        return obj.empleado.apellido_paterno
    empleado_apellido_paterno.short_description = 'Apellido Paterno'

    def empleado_apellido_materno(self, obj):
        return obj.empleado.apellido_materno
    empleado_apellido_materno.short_description = 'Apellido Materno'

    def empleado_nombres(self, obj):
        return obj.empleado.nombres
    empleado_nombres.short_description = 'Nombres'

@admin.register(GrupoHistorial)
class GrupoHistorialAdmin(admin.ModelAdmin):
    list_display = ('empleado_numero_documento', 'empleado_apellido_paterno', 'empleado_apellido_materno', 'empleado_nombres', 'denominacion', 'fecha_inicio', 'fecha_fin')
    search_fields = ('empleado__numero_documento', 'empleado__apellido_paterno', 'empleado__apellido_materno', 'empleado__nombres')
    
    def empleado_numero_documento(self, obj):
        return obj.empleado.numero_documento
    empleado_numero_documento.short_description = 'DNI'
    
    def empleado_apellido_paterno(self, obj):
        return obj.empleado.apellido_paterno
    empleado_apellido_paterno.short_description = 'Apellido Paterno'

    def empleado_apellido_materno(self, obj):
        return obj.empleado.apellido_materno
    empleado_apellido_materno.short_description = 'Apellido Materno'

    def empleado_nombres(self, obj):
        return obj.empleado.nombres
    empleado_nombres.short_description = 'Nombres'
    
@admin.register(CargoHistorial)
class CargoHistorialAdmin(admin.ModelAdmin):
    list_display = ('empleado_numero_documento', 'empleado_apellido_paterno', 'empleado_apellido_materno', 'empleado_nombres', 'denominacion', 'fecha_inicio', 'fecha_fin')
    search_fields = ('empleado__numero_documento', 'empleado__apellido_paterno', 'empleado__apellido_materno', 'empleado__nombres')
    
    def empleado_numero_documento(self, obj):
        return obj.empleado.numero_documento
    empleado_numero_documento.short_description = 'DNI'
    
    def empleado_apellido_paterno(self, obj):
        return obj.empleado.apellido_paterno
    empleado_apellido_paterno.short_description = 'Apellido Paterno'

    def empleado_apellido_materno(self, obj):
        return obj.empleado.apellido_materno
    empleado_apellido_materno.short_description = 'Apellido Materno'

    def empleado_nombres(self, obj):
        return obj.empleado.nombres
    empleado_nombres.short_description = 'Nombres'
    
@admin.register(NivelHistorial)
class NivelHistorialAdmin(admin.ModelAdmin):
    list_display = ('empleado_numero_documento', 'empleado_apellido_paterno', 'empleado_apellido_materno', 'empleado_nombres', 'denominacion', 'fecha_inicio', 'fecha_fin')
    search_fields = ('empleado__numero_documento', 'empleado__apellido_paterno', 'empleado__apellido_materno', 'empleado__nombres')
    
    def empleado_numero_documento(self, obj):
        return obj.empleado.numero_documento
    empleado_numero_documento.short_description = 'DNI'
    
    def empleado_apellido_paterno(self, obj):
        return obj.empleado.apellido_paterno
    empleado_apellido_paterno.short_description = 'Apellido Paterno'

    def empleado_apellido_materno(self, obj):
        return obj.empleado.apellido_materno
    empleado_apellido_materno.short_description = 'Apellido Materno'

    def empleado_nombres(self, obj):
        return obj.empleado.nombres
    empleado_nombres.short_description = 'Nombres'

@admin.register(PlazaHistorial)
class PlazaHistorialAdmin(admin.ModelAdmin):
    list_display = ('empleado_numero_documento', 'empleado_apellido_paterno', 'empleado_apellido_materno', 'empleado_nombres', 'denominacion', 'fecha_inicio', 'fecha_fin')
    search_fields = ('empleado__numero_documento', 'empleado__apellido_paterno', 'empleado__apellido_materno', 'empleado__nombres')
    
    def empleado_numero_documento(self, obj):
        return obj.empleado.numero_documento
    empleado_numero_documento.short_description = 'DNI'
    
    def empleado_apellido_paterno(self, obj):
        return obj.empleado.apellido_paterno
    empleado_apellido_paterno.short_description = 'Apellido Paterno'

    def empleado_apellido_materno(self, obj):
        return obj.empleado.apellido_materno
    empleado_apellido_materno.short_description = 'Apellido Materno'

    def empleado_nombres(self, obj):
        return obj.empleado.nombres
    empleado_nombres.short_description = 'Nombres'
    
    
