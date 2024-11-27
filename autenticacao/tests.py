from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from unittest.mock import patch
from io import BytesIO
from fpdf import FPDF
from autenticacao.forms import PerfilForm
from django.contrib.auth import get_user_model


class HomeViewTests(TestCase):
    def test_home_view_template_render(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')

class SobreNosViewTests(TestCase):
    def test_sobre_view_template_render_and_context(self):
        response = self.client.get(reverse('sobre'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/sobre.html')
        self.assertEqual(response.context['pagina_atual'], 'sobre')

class SuporteViewTests(TestCase):
    def test_suporte_view_template_render_and_context(self):
        response = self.client.get(reverse('suporte'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/suporte.html')
        self.assertEqual(response.context['pagina_atual'], 'suporte')

