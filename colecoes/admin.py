from django.contrib import admin
from colecoes.models import Colecao, Item

@admin.register(Colecao)
class ColecaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'categoria', 'usuario')
    list_filter = ('categoria', 'usuario')
    search_fields = ('nome', 'descricao')
    date_hierarchy = 'data_criacao'

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'categoria', 'colecao')
    list_filter = ('categoria', 'colecao')
    search_fields = ('nome', 'descricao')
    date_hierarchy = 'data_aquisicao'
    readonly_fields = ('foto',)