from django.conf import settings
from django.db import models
from django.core.mail import send_mail

class Acidente(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    data_ocorrencia = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

class MensagemAcidente(models.Model):
    acidente = models.ForeignKey(Acidente, on_delete=models.CASCADE, related_name='mensagens')
    conteudo = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)
    enviado_para = models.EmailField()

    def __str__(self):
        return f"Mensagem para {self.enviado_para} sobre {self.acidente.titulo}"

    def enviar_email(self):
        try:
            send_mail(
                f"Informações sobre o acidente: {self.acidente.titulo}",
                self.conteudo,
                settings.EMAIL_HOST_USER,
                [self.enviado_para],
                fail_silently=False,
            )
        except Exception as e:
            raise Exception(f"Erro ao enviar o e-mail: {e}")
