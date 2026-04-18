from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from example.models import HistoricoTesouro

# login screen

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # redirect based on role
            if user.is_staff or user.is_superuser:
                return redirect('home_admin')
            else:
                return redirect('home_user')
    else:
        form = AuthenticationForm()
    return render(request, 'frontend/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def home_user(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.is_staff or request.user.is_superuser:
        return redirect('home_admin')
    return render(request, 'frontend/home_user.html', {'system_name': 'Tesouro App'})


def home_admin(request):
    if not request.user.is_authenticated or not (request.user.is_staff or request.user.is_superuser):
        return redirect('login')
    return render(request, 'frontend/home_admin.html', {'system_name': 'Tesouro App'})


def titles_visualization(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.is_staff or request.user.is_superuser:
        return redirect('home_admin')
    
    # Buscar o último registro de HistoricoTesouro
    ultimo = HistoricoTesouro.objects.order_by('-data_captura').first()
    titulos = []
    if ultimo:
        payload = ultimo.payload_cru
        for category in ['TesouroLegado', 'Tesouro24x7']:
            if payload.get(category):
                for titulo in payload[category]:
                    # Determinar grupo e cor
                    name = titulo['treasuryBondName']
                    if 'Selic' in name:
                        group = 'Selic'
                        color = 'primary'  # azul
                    elif 'Prefixado' in name:
                        group = 'Prefixado'
                        color = 'success'  # verde
                    elif 'IPCA' in name:
                        group = 'IPCA'
                        color = 'danger'  # vermelho
                    elif 'Renda' in name or 'Educa' in name:
                        group = 'Especial'
                        color = 'warning'  # amarelo
                    else:
                        group = 'Outros'
                        color = 'secondary'  # cinza
                    
                    titulos.append({
                        'name': name,
                        'profitability': titulo.get('investmentProfitabilityIndexerName', 'N/A'),
                        'value': titulo.get('unitaryInvestmentValue', 0),
                        'group': group,
                        'color': color
                    })
    
    return render(request, 'frontend/titles_visualization.html', {'titulos': titulos})


