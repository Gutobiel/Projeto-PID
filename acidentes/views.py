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

# View para enviar uma nova mensagem relacionada a um acidente
class EnviarMensagemView(LoginRequiredMixin, FormView):
    login_url = reverse_lazy('login')
    template_name = 'acidentes/enviar_mensagem.html'
    form_class = MensagemAcidenteForm
    success_url = reverse_lazy('sucesso')

    def form_valid(self, form):
        conteudo = form.cleaned_data['conteudo']
        email_destinatario = form.cleaned_data['enviado_para']
        acidente = get_object_or_404(Acidente, id=self.kwargs['acidente_id'])

        # Enviar o e-mail
        try:
            send_mail(
                subject=f'Nova Mensagem sobre o Acidente: {acidente.titulo}', 
                message=conteudo,  
                from_email=settings.EMAIL_HOST_USER,  
                recipient_list=[email_destinatario],  
                fail_silently=False,
            )
        except Exception as e:
            form.add_error(None, f"Erro ao enviar o e-mail: {e}")
            return self.form_invalid(form)

        # Salvar a mensagem no banco de dados associada ao acidente
        MensagemAcidente.objects.create(
            acidente=acidente, 
            conteudo=conteudo, 
            enviado_para=email_destinatario
        )

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        acidente = get_object_or_404(Acidente, id=self.kwargs['acidente_id'])
        context['acidente'] = acidente
        context['ultima_mensagem'] = MensagemAcidente.objects.filter(acidente=acidente).last()
        return context

# View para reenviar a última mensagem associada a um acidente específico
class ReenviarUltimaMensagemView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'acidentes/enviar_mensagem.html'

    def post(self, request, acidente_id):
        acidente = get_object_or_404(Acidente, id=acidente_id)
        ultima_mensagem = MensagemAcidente.objects.filter(acidente=acidente).last()

        if ultima_mensagem:
            try:
                send_mail(
                    f"Reenvio da Mensagem sobre: {acidente.titulo}",
                    ultima_mensagem.conteudo,
                    settings.DEFAULT_FROM_EMAIL,
                    [ultima_mensagem.enviado_para],
                    fail_silently=False,
                )
                return redirect('sucesso')
            except Exception as e:
                return render(request, self.template_name, {'error': f'Erro ao reenviar a mensagem: {e}'})
        else:
            return render(request, self.template_name, {'error': 'Nenhuma mensagem encontrada para reenviar.'})
