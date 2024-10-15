from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Semaforo
from .forms import SemaforoForm
from django.contrib.auth.mixins import LoginRequiredMixin
       
class PaginaSemaforoView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    template_name = 'semaforos/semaforo.html'
    model = Semaforo
    context_object_name = 'semaforos' 
    


class AdicionarSemaforoView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    template_name = 'semaforos/adicionar-semaforo.html'
    form_class = SemaforoForm
    success_url = reverse_lazy('semaforo') 


class AtualizarSemaforoView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    template_name = 'semaforos/atualizar-semaforo.html'
    model = Semaforo
    form_class = SemaforoForm
    success_url = reverse_lazy('semaforo')

class DeletarSemaforoView(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    template_name = 'semaforos/deletar-semaforo.html'
    model = Semaforo
    success_url = reverse_lazy('semaforo')
