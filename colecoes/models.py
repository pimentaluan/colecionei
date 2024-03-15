from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

class Publicacao(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='publicacoes')
    texto = models.TextField()
    imagem = models.ImageField(upload_to='publicacoes/', null=True, blank=True)
    data_publicacao = models.DateTimeField(auto_now_add=True)
    publicada = models.BooleanField(default=False)

    def __str__(self):
        return f'Publicação por {self.autor.username} em {self.data_publicacao}'

@receiver(post_save, sender=Publicacao)
def definir_autor(sender, instance, created, **kwargs):
    if created:
        instance.autor = get_user_model().objects.get(id=instance.autor.id)
        instance.save()
