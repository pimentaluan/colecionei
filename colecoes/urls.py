from django.urls import path
from . import views
from colecoes.views import feed, colecao, nova_colecao, novo_item, meu_perfil, perfil, buscar, like_colecao, salvar_colecao, comentar_colecao

urlpatterns = [
    path('feed/', feed, name='feed'),
    path('buscar', buscar, name='buscar'),
    path('colecao/<str:username>/<int:colecao_id>/', colecao, name='colecao'),
    path('nova-colecao/', nova_colecao, name='nova-colecao'),
    path('novo-item/<str:username>/<int:colecao_id>/', novo_item, name='novo-item'),
    path('perfil/', meu_perfil, name='meu-perfil'),
    path('perfil/<int:usuario_id>/', perfil, name='perfil'),
    path('colecao/<int:colecao_id>/like/', views.like_colecao, name='like-colecao'),
    path('colecao/<int:colecao_id>/salvar/', views.salvar_colecao, name='salvar-colecao'),
    path('colecao/<int:colecao_id>/comentar/', views.comentar_colecao, name='comentar-colecao'),
]