from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    # Método auxiliar para verificar se o usuário tem um papel específico por nome
    def has_role(self, role_name):
        return self.groups.filter(name=role_name).exists()

    @property
    def roles(self):
        return self.groups.all()


class Formulario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='formularios')
    created_at = models.DateTimeField(auto_now_add=True)
    descricao = models.TextField()

    class Meta:
        verbose_name = 'Formulário'
        verbose_name_plural = 'Formulários'

    def __str__(self):
        return f"Formulário de {self.user.username} em {self.created_at}"