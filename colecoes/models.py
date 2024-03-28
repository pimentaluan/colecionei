from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.conf import settings


class Publicacao(models.Model):
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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