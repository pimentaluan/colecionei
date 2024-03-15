from django.urls import path, include
from usuarios.views import login, cadastro, logout

urlpatterns = [
    path('', login, name='login'),
    path('accounts/', include('allauth.urls')),
    path('cadastro', cadastro, name='cadastro'),
    path('logout', logout, name='logout'),
]