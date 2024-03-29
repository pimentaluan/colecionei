from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

def upload_to(instance, filename):
    return f'fotos/{datetime.now().year}/{instance.id}/{filename}'

class Usuario(AbstractUser):
    DEFAULT_PHOTO_PATH = "static 'assets/icones/coroa.svg'"
    photo = models.ImageField(upload_to=upload_to, blank=True)
    birth_date = models.DateField(blank=True, null=True)