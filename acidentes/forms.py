from django import forms
from .models import MensagemAcidente

class MensagemAcidenteForm(forms.ModelForm):
    class Meta:
        model = MensagemAcidente
        fields = ['conteudo', 'enviado_para']
        widgets = {
            'conteudo': forms.Textarea(attrs={'placeholder': 'Escreva sua mensagem aqui...'}),
            'enviado_para': forms.EmailInput(attrs={'placeholder': 'Digite o e-mail do destinatário'}),
        }
