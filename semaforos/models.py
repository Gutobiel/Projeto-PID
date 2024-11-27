from django.db import models

class Semaforo(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    endereco = models.CharField(max_length=255)
    tipo = models.CharField(max_length=50)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    #adicionado
    nome = models.CharField(max_length=100, default='Default Name')
    status = models.CharField(max_length=50)  # Confirme se o campo existe e o tipo está correto

    def __str__(self):
        return self.codigo