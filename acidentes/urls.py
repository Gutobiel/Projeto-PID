from django.urls import path
from .views import PaginaAcidentesView
from acidentes import views

urlpatterns = [
    path('acidentes/', PaginaAcidentesView.as_view(), name='acidentes'),
     path('enviar_mensagem/', views.enviar_mensagem, name='enviar_mensagem'),
]
