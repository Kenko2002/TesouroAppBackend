#!/bin/bash


# Instala as dependências
echo "Installing requirements..."
pip install -r requirements.txt --break-system-packages

# Coleta os arquivos estáticos
echo "Collecting static files..."
python3 manage.py collectstatic --noinput --clear


echo "Build process completed!"