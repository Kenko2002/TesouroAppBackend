#!/bin/bash


# Instala as dependências
echo "Installing requirements..."
pip install -r requirements.txt --break-system-packages

# Executa migrações
echo "Running migrations..."
python3 manage.py makemigrations
python3 manage.py migrate

# Garante que exista um superusuário padrão
# NOTE: as credenciais devem ser mantidas seguras em produção!
echo "Creating default superuser if not exists..."
python3 manage.py shell <<'PYTHON'
from django.contrib.auth import get_user_model
User = get_user_model()
username = 'admin'
password = 'admin@123'
email = 'admin@example.com'
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print('Superuser created.')
else:
    print('Superuser already exists.')
PYTHON

# Coleta os arquivos estáticos
echo "Collecting static files..."
python3 manage.py collectstatic --noinput --clear


echo "Build process completed!"