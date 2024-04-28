from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

def upload_to(instance, filename):
    return f'fotos/{datetime.now().year}/{instance.id}/{filename}'

class Usuario(AbstractUser):
    DEFAULT_PHOTO_PATH = "static 'assets/icones/coroa.svg'"
    nome_completo = models.CharField(max_length=255, blank=True)
    biografia = models.TextField(blank=True)
    photo = models.ImageField(upload_to=upload_to, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    seguindo = models.ManyToManyField('self', related_name='seguidores', symmetrical=False)
    colecoes_salvas = models.ManyToManyField('colecoes.Colecao', related_name='usuarios_que_salvaram')
    def esta_seguindo(self, usuario):
        return self.seguindo.filter(id=usuario.id).exists()
    
    def primeiro_nome(self):
        return self.nome_completo.split(' ')[0]