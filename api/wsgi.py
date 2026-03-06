import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nome_do_seu_projeto.settings') # Substitua pelo nome real do seu projeto

application = get_wsgi_application()

# Isso faz o WhiteNoise servir os arquivos da pasta 'staticfiles' na raiz
app = WhiteNoise(application, root=os.path.join(os.path.dirname(__file__), '../staticfiles'))
app.add_files(os.path.join(os.path.dirname(__file__), '../static'), prefix='static/')