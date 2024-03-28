from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

def upload_to(instance, filename):
    return 'fotos/%s/%s/%s/%s' % (datetime.now().year, instance.get_full_name(), filename)

class Usuario(AbstractUser):
    photo = models.ImageField(upload_to=upload_to, blank=True)
    birth_date = models.DateField(blank=True, null=True)