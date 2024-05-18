from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

def upload_to(instance, filename):
    username = instance.username.replace('?', '_')
    return f'foto_user/{username}/{datetime.now().year}/{filename}'

class Usuario(AbstractUser):
    DEFAULT_PHOTO_PATH = "static 'assets/icones/coroa.svg'"
    nome_completo = models.CharField(max_length=255, blank=True)
    biografia = models.TextField(blank=True)
    photo = models.ImageField(upload_to=upload_to, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    seguindo = models.ManyToManyField('self', related_name='+', symmetrical=False, blank=True)
    seguidores = models.ManyToManyField('self', related_name='+', symmetrical=False, blank=True)
    colecoes_salvas = models.ManyToManyField('colecoes.Colecao', related_name='usuarios_que_salvaram', blank=True)
    def esta_seguindo(self, usuario):
        return self.seguindo.filter(id=usuario.id).exists()
    
    def primeiro_nome(self):
        return self.nome_completo.split(' ')[0]
    
    def get_nome_completo(self):
        if self.nome_completo:
            return self.nome_completo
        else:
            return f"{self.first_name} {self.last_name}"