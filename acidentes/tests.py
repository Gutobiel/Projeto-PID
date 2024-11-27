from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail
from django.contrib.auth.models import User
from semaforos.models import Semaforo
from .models import MensagemAcidente
from django.contrib.auth import get_user_model
from cadastros.models import Orgao


class EnviarMensagemViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('enviar_mensagem')  # Altere para o nome correto da URL do envio de mensagens
        self.mensagem = "Mensagem de teste de acidente"
        self.destinatario = 'samuelssf027@gmail.com'

    def test_envio_mensagem_sucesso(self):
        with self.settings(
            EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
            EMAIL_HOST_USER='test@example.com'
        ):
            response = self.client.post(self.url, {'mensagem': self.mensagem})

            # Verifica se o e-mail foi enviado
            self.assertEqual(len(mail.outbox), 1)
            email = mail.outbox[0]
            self.assertEqual(email.subject, "Nova mensagem de acidente")
            self.assertEqual(email.body, self.mensagem)
            self.assertIn(self.destinatario, email.to)
            
            # Verifica o redirecionamento com mensagem de sucesso
            self.assertContains(response, "Mensagem enviada com sucesso!")

    def test_envio_mensagem_falha(self):
        with self.settings(
            EMAIL_BACKEND='django.core.mail.backends.dummy.DummyBackend',
            EMAIL_HOST_USER='test@example.com'
        ):
            response = self.client.post(self.url, {'mensagem': self.mensagem})
            
            # Verifica se ocorre erro no envio de mensagem
            self.assertEqual(response.status_code, 200)
            self.assertIn("Erro ao enviar mensagem", response.content.decode())
