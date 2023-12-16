from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    nome = models.CharField(max_length=255)
    numero_telefone = models.CharField(max_length=15)
    email = models.EmailField(unique=True, blank=False)

    username = models.CharField(max_length=30, unique=False, blank=True)

    def __str__(self):
        return self.email  
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Produto(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    preco = models.FloatField()
    quantidade = models.IntegerField()
    imagem = models.ImageField(upload_to='produtos', blank=True)

    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

class Vendas(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    total = models.FloatField()
    data = models.DateTimeField(auto_now_add=True)

    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.produto.titulo
