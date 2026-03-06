
# Instala as dependências
echo "Installing pip..."
python3 -m pip install --upgrade pip

echo "Installing requirements..."
python3 -m pip install -r requirements.txt

# Coleta os arquivos estáticos
echo "Collecting static files..."
python3 manage.py collectstatic --noinput --clear