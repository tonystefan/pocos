from django.db import models
from django.contrib.auth.models import User

class Modulo(models.Model):
    """
    Representa um módulo ou funcionalidade da aplicação.
    """
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Módulo"
        verbose_name_plural = "Módulos"

    def __str__(self):
        return self.nome

class PermissaoModulo(models.Model):
    """
    Associa um usuário a um módulo, concedendo acesso.
    """
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='permissoes_modulos')
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('usuario', 'modulo')
        verbose_name = "Permissão de Módulo"
        verbose_name_plural = "Permissões de Módulos"

    def __str__(self):
        return f"{self.usuario.username} pode acessar {self.modulo.nome}"
