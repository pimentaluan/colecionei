from django.urls import path
from colecoes.views import feed, nova_colecao, novo_item

urlpatterns = [
    path('feed', feed, name='feed'),
    path('nova-colecao', nova_colecao, name='nova-colecao'),
    path('novo-item/<str:username>/<int:colecao_id>/', novo_item, name='novo-item'),
]