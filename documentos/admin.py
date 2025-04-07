from django.contrib import admin
from .models import Resolucion

@admin.register(Resolucion)
class ResolucionAdmin(admin.ModelAdmin):
    list_display = ('documento', 'numero', 'fecha', 'ver_pdf')
    search_fields = ('documento', 'numero', 'fecha')

