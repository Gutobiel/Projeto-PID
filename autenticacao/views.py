from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
import pandas as pd
from fpdf import FPDF
from django.http import HttpResponse

from autenticacao.forms import PerfilForm

class HomeView(TemplateView):
    template_name = 'home/index.html'

class SobreNosView(TemplateView):
    template_name = 'home/sobre.html'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['pagina_atual'] = 'sobre'
        return contexto

class SuporteView(TemplateView):
    template_name = 'home/suporte.html'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['pagina_atual'] = 'suporte'
        return contexto




class MenuPrincipalView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'pagina-menu/pagina-menu.html'

class AdminPaginaView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'pagina-admin/admin.html'

class PerfilView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'pagina-perfil/perfil.html'


    def get(self, request, *args, **kwargs):
        user = request.user
        form = PerfilForm(instance=user)
        return render(request, self.template_name, {'form': form})
    

class RelatorioView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'pagina-relatorio/relatorio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtém a URL da página anterior do cabeçalho HTTP Referer
        referer = self.request.META.get('HTTP_REFERER')
        
        # Se houver uma URL anterior, adicione-a aos breadcrumbs
        breadcrumb_items = [{'name': 'Menu', 'link': reverse('menu-principal')}]
        if referer:
            breadcrumb_items.append({'name': 'Voltar', 'link': referer})
        
        breadcrumb_items.append({'name': 'Relatório', 'link': None})
        
        context['breadcrumb_items'] = breadcrumb_items
        return context

    def gerar_pdf(self):
        # Exemplo de dados, pode ser substituído pelo seu dataframe
        data = {
            'Tipo de Veículo': ['Motos', 'Carros', 'Caminhões'],
            'Quantidade': [120, 350, 45]
        }
        df = pd.DataFrame(data)

        # Gerar o PDF usando FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Adicionar título ao PDF
        pdf.cell(200, 10, txt="Relatório de Veículos", ln=True, align='C')

        # Adicionar os dados do dataframe ao PDF
        for index, row in df.iterrows():
            pdf.cell(200, 10, txt=f"{row['Tipo de Veículo']}: {row['Quantidade']}", ln=True)

        # Criar a resposta HTTP para o PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="relatorio_veiculos.pdf"'
        pdf.output(dest='F').encode('latin1')  # Salvar no destino correto para enviar a resposta
        response.write(pdf.output(dest='S').encode('latin1'))
        return response




