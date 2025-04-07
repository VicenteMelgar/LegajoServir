from django.urls import path
from .import views 

app_name='empleados'

urlpatterns = [
  path('', views.datospersonales_lista, name='datos_personales'),
  path('historial/<int:empleado_id>/', views.info_historial, name='info_historial'),
]

