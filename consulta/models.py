from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.timezone import now


class Emitente(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    nome = models.CharField(
        max_length=100
    )
    fantasia = models.CharField(
        max_length=100
    )
    cnpj = models.CharField(
        max_length=20
    )
    cidade = models.CharField(
        max_length=50
    )
    estado = models.CharField(
        max_length=20
    )
    endereco = models.CharField(
        max_length=250
    )
    publicacao = models.DateTimeField(default=now, editable=False)
    
    def __str__(self):
        return self.fantasia

class Nota(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
        )
    mercado = models.ForeignKey(
        Emitente,
        on_delete=models.CASCADE
        )
    dataCompra = models.DateTimeField()
    publicacao = models.DateTimeField(default=now, editable=False)
    chave = models.CharField(
        max_length=50
    )

    def __str__(self):
        return self.chave

   
class Produto(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL       
        )
    nota = models.ForeignKey(
        Nota,
        on_delete=models.CASCADE
        )
    nome = models.CharField(
        max_length=200
        )
    preco = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=False,
        blank=False
    )
    data = models.DateTimeField(
        default = timezone.now()
    )
    def __str__(self):
        return self.nome