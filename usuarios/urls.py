from django.urls import path, include
from usuarios.views import login, cadastro, logout, seguir_usuario, deixar_seguir_usuario
from . import views


urlpatterns = [
    path('', login, name='login'),
    path('accounts/', include('allauth.urls')),
    path('cadastro', cadastro, name='cadastro'),
    path('logout', logout, name='logout'),
    path('seguir/<int:usuario_id>/', views.seguir_usuario, name='seguir_usuario'),
    path('deixar_seguir_usuario/<int:usuario_id>/', views.deixar_seguir_usuario, name='deixar_seguir_usuario'),
]