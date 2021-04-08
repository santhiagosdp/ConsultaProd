from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Produto(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #author = models.OneToOneField(User, related_name='profile',on_delete=models.CASCADE)
    mercado = models.CharField(max_length=100)
    fantasia = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=20, default="null")
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=20)
    endereco = models.CharField(max_length=250)
    nomeProduto = models.CharField(max_length=200)
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    dataCompra = models.DateTimeField()
    dataPublicacao = models.DateTimeField()
    chave = models.CharField(max_length=50)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.nomeProduto
