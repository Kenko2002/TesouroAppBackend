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


    
    
class HistoricoTesouro(models.Model):
    # JSONField armazena o dicionário completo (suportado nativamente no Postgres, SQLite e MySQL)
    payload_cru = models.JSONField(verbose_name="Dados Brutos do Tesouro")
    data_captura = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Histórico do Tesouro'
        verbose_name_plural = 'Históricos do Tesouro'
        ordering = ['-data_captura']

    def __str__(self):
        return f"Captura em {self.data_captura.strftime('%d/%m/%Y %H:%M')}"