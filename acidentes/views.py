from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from semaforos.models import Semaforo
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from .models import MensagemAcidente, Acidente
from .forms import MensagemAcidenteForm

# View principal que mostra a página de acidentes
class PaginaAcidentesView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'acidentes/acidentes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Recupera todos os semáforos
        semaforos = Semaforo.objects.all()
        # Adiciona os semáforos ao contexto
        context['semaforos'] = semaforos
        return context

def enviar_mensagem(request):
    if request.method == 'POST':
        mensagem = request.POST.get('mensagem')
        assunto = "Nova mensagem de acidente"
        destinatario = 'samuelssf027@gmail.com'
        
        try:
            send_mail(
                assunto,
                mensagem,
                settings.EMAIL_HOST_USER,
                [destinatario],
                fail_silently=False,
            )
            # HTML com redirecionamento automático após 3 segundos
            return HttpResponse("""
                <p>Mensagem enviada com sucesso! Você será redirecionado em 3 segundos...</p>
                <script>
                    setTimeout(function() {
                        window.location.href = '/acidentes/';
                    }, 3000);
                </script>
            """)
        except Exception as e:
            return HttpResponse(f'Erro ao enviar mensagem: {e}')
    
    return redirect('acidentes.html')