from django.contrib import admin
from colecoes.models import Categoria, Colecao, Item, Comentario

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

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'imagem_padrao')
    search_fields = ('nome',)

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'colecao', 'texto')
    list_filter = ('usuario', 'colecao')
    search_fields = ('texto',)