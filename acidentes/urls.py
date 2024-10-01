from django.urls import path
from .views import PaginaAcidentesView, EnviarMensagemView, ReenviarUltimaMensagemView

urlpatterns = [
    path('acidentes/', PaginaAcidentesView.as_view(), name='acidentes'),
    path('enviar-mensagem/<int:acidente_id>/', EnviarMensagemView.as_view(), name='enviar_mensagem'),
    path('reenviar-mensagem/<int:acidente_id>/', ReenviarUltimaMensagemView.as_view(), name='reenviar_mensagem'),
]
