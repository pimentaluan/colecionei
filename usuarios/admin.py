from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'birth_date', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('photo', 'birth_date', 'biografia', 'nome_completo','seguidores')}),
    )

admin.site.register(Usuario, UsuarioAdmin)