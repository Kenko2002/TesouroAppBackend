from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Adiciona campos personalizados se necessário
    # Por exemplo, um campo adicional
    bio = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'