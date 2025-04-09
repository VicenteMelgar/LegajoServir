from django.urls import path
from .import views 
from .views import CustomLoginView
from django.contrib.auth.views import LogoutView

app_name='legajos'

urlpatterns = [
  path('', views.legajos_lista, name='legajos_lista'),
  path('info_general/<int:legajo_id>', views.info_general, name='info_general'),
  path('documentos/', views.documentos, name='documentos'),
  path('dashboard/', views.dashboard, name='dashboard'),
  path('login/', CustomLoginView.as_view(), name='login'),
  path('logout/', LogoutView.as_view(), name='logout'),
]

