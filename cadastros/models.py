from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import random
import string
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password


def generate_random_string(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

def generate_random_password():
    return generate_random_string(10)

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(username, email, password, **extra_fields)

class Cargo(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class Orgao(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class TipoAcesso(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class CustomUser(AbstractBaseUser, PermissionsMixin):
    nome_completo = models.CharField(max_length=100, help_text="Digite o nome completo")
    username = models.CharField(max_length=8, unique=True, default=generate_random_string)
    email = models.EmailField(unique=True, help_text="Digite o email")
    celular = models.CharField(max_length=15, default='')  # Valor padrão vazio para o celular
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, default=1, help_text="Selecione o cargo...")  # Valor padrão de 1 para o cargo
    orgao = models.ForeignKey(Orgao, on_delete=models.CASCADE, default=1, help_text="Selecione o orgão...")  # Valor padrão de 1 para o orgão
    setor = models.CharField(max_length=100, default='')  # Valor padrão vazio para o setor
    STATUS_CHOICES = [
        (True, 'Ativo'),
        (False, 'Inativo'),
    ] 
    status = models.BooleanField(default=True, choices=STATUS_CHOICES)  # Valor padrão de True para o status
    observacoes = models.TextField(blank=True, null=True, default='', help_text="Adicione quaisquer observações adicionais sobre o usuário")  # Valor padrão vazio para as observações
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def save(self, *args, **kwargs):
        if not self.pk:  # Apenas para novos usuários
            password = generate_random_password()
            self.set_password(password)
            send_mail(
                'Cadastro realizado com sucesso - Bem-vindo ao Vrum Vrum',
                f'Olá,\n\nParabéns! Seu cadastro no Vrum Vrum foi realizado com sucesso!\n\n'
                f'Aqui estão seus detalhes de login:\n\nLogin: {self.username}\n'
                f'Senha: {password}\n\nAgora você pode acessar sua conta no Vrum Vrum e começar a explorar todos os recursos disponíveis.\n\n'
                'Obrigado por se juntar a nós!\n\nAtenciosamente,\nEquipe Vrum Vrum',
                settings.EMAIL_HOST_USER,
                [self.email],
                fail_silently=False,
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome_completo
