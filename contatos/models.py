from mailbox import NotEmptyError
from django.db import models
from django.utils import timezone
# Create your models here.


class Categoria(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome


class Contato(models.Model):
    nome = models.CharField(max_length=255)
    sobrenome = models.CharField(blank=True, null=True, max_length=255)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True, max_length=255)
    data_criacao = models.DateTimeField(default=timezone.now)
    descricao = models.TextField(blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    mostrar = models.BooleanField(default=True)
    foto = models.ImageField(blank=True, null=True, upload_to='fotos/%Y/%m/')

    def __str__(self):
        return self.nome
