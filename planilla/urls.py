from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_usuario, name='login_usuario'),
    path('logout/', views.logout_usuario, name='logout_usuario'),    
    path('altas/nueva/', views.altas_nueva, name='altas_nueva'),
    path('altas/lista/', views.altas_lista, name='altas_lista'),
    path('plazas/', views.altas_lista, name='control_plazas'),
    path('', views.lista_planilla, name='planilla'),
    path('anexo-ejecucion/', views.anexo_ejecucion, name='anexo_ejecucion'),
    path('historial/', views.historial, name='historial'),
    path('debug-planteles/', views.debug_planteles),
    path('planilla/eliminar/<int:no>/', views.eliminar_registro, name='eliminar_registro'),
    path('consulta/', views.consulta, name='consulta'),
    path('estadisticas/', views.estadisticas, name='estadisticas'),
    path('debug-planteles/', views.dplanteles, name='dplanteles'),
    path('directorio/', views.directorio, name='directorio'),
]