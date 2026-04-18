from django.core.management.base import BaseCommand
import requests
from example.models import HistoricoTesouro

class Command(BaseCommand):
    help = 'Busca dados do Tesouro Direto e salva no banco'

    def handle(self, *args, **options):
        url = "https://www.tesourodireto.com.br/o/rentabilidade/investir"
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        self.stdout.write("Iniciando captura...")
        
        try:
            response = requests.get(url, headers=headers)
            data = response.json()
            HistoricoTesouro.objects.create(payload_cru=data)
            self.stdout.write(self.style.SUCCESS('Dados capturados com sucesso!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro: {e}'))