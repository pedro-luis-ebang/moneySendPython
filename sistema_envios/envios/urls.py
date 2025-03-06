from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registrar/', views.registrar_usuario, name='registrar_usuario'),
    path('enviar/', views.enviar_dinero, name='enviar_dinero'),
    path('depositar/', views.depositar_dinero, name='depositar_dinero'),
    path('retirar/', views.retirar_dinero, name='retirar_dinero'),
    path('pagar/', views.pagar_servicio, name='pagar_servicio'),
    path('historial/<int:usuario_id>/', views.ver_historial, name='ver_historial'),
    path('grafico/', views.ver_grafico, name='ver_grafico'),
    path('datos_grafico/', views.datos_grafico, name='datos_grafico'),
    path('eliminar_usuario/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
]
