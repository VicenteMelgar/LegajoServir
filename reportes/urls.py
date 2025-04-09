from django.urls import path
from . import views

app_name = 'reportes'

urlpatterns = [
    path('', views.formulario_reportes, name='formulario_reportes'),
    path('constancia/<int:id_empleado>/', views.generar_constancia, name='generar_constancia'),
    path('descargar_constancia/<int:empleado_id>/', views.descargar_constancia, name='descargar_constancia'),
    path('informe/<int:id_empleado>/', views.generar_informe, name='generar_informe'),
    path('descargar_informe/<int:empleado_id>/', views.descargar_informe, name='descargar_informe'),
]