from django.urls import path
from semaforos.views import AdicionarSemaforoView, AtualizarSemaforoView, DeletarSemaforoView, PaginaSemaforoView
from . import views

urlpatterns = [
     path('semaforo/', PaginaSemaforoView.as_view(), name='semaforo'),
     path('adicionar-semaforo/', AdicionarSemaforoView.as_view(), name='adicionar-semaforo'),
     path('atualizar-semaforo/<int:pk>/', AtualizarSemaforoView.as_view(), name='atualizar-semaforo'),
     path('deletar-semaforo/<int:pk>/', DeletarSemaforoView.as_view(), name='deletar-semaforo'),
     
]
