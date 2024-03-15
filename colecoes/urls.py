from django.urls import path
from colecoes.views import feed

urlpatterns = [
    path('feed', feed, name='feed'),
]