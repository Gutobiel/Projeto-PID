from django.test import TestCase
from .models import Semaforo

class SemaforoModelTestCase(TestCase):
    def test_salvar_semaforo(self):
        """Verifica se o semáforo é salvo no banco de dados."""
        
        # Cria um semáforo com os campos corretos
        semaforo = Semaforo.objects.create(
            codigo='SEM123',
            endereco='Rua ABC, 123',
            tipo='Sinal de Trânsito',
            marca='Marca A',
            modelo='Modelo X',
            nome='Semáforo Principal',
            status='Ativo'
        )

        # Verifica se o semáforo foi salvo no banco de dados
        self.assertEqual(Semaforo.objects.count(), 1)  # Verifica se há 1 semáforo no banco
        self.assertEqual(semaforo.codigo, 'SEM123')  # Verifica o valor do campo codigo
        self.assertEqual(semaforo.endereco, 'Rua ABC, 123')  # Verifica o valor do campo endereco
        self.assertEqual(semaforo.tipo, 'Sinal de Trânsito')  # Verifica o valor do campo tipo
        self.assertEqual(semaforo.marca, 'Marca A')  # Verifica o valor do campo marca
        self.assertEqual(semaforo.modelo, 'Modelo X')  # Verifica o valor do campo modelo
        self.assertEqual(semaforo.nome, 'Semáforo Principal')  # Verifica o valor do campo nome
        self.assertEqual(semaforo.status, 'Ativo')  # Verifica o valor do campo status
