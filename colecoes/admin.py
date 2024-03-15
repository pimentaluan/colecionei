from django.contrib import admin
from colecoes.models import Publicacao

class ListaPublicacoes(admin.ModelAdmin):
    list_display = ("id","autor", "texto", "data_publicacao", "publicada")
    list_display_links = ("id", "autor")
    search_fields = ("autor",)
    list_filter = ("publicada",)
    list_editable = ("publicada",)
    list_per_page = 10

admin.site.register(Publicacao, ListaPublicacoes)