from django.apps import AppConfig as DjangoAppConfig # Importe com alias para não confundir
import os

class ExampleConfig(DjangoAppConfig): # Mude o nome da classe para ExampleConfig
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'example' # O NOME DA PASTA DO SEU APP

    def ready(self):
        # O Django executa o ready() duas vezes no modo reload (runserver). 
        # O check abaixo garante que o scheduler só ligue uma vez.
        if os.environ.get('RUN_MAIN') == 'true':
            try:
                # Importação relativa para o arquivo scheduler.py que está na mesma pasta
                from .scheduler import start_scheduler
                start_scheduler()
                print("--- Scheduler do Tesouro Iniciado com Sucesso ---")
            except Exception as e:
                print(f"--- Erro ao iniciar Scheduler: {e} ---")