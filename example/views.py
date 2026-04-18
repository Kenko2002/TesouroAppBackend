# example/views.py
from datetime import datetime
from django.http import HttpResponse
from rest_framework.views import APIView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .serializers import UserSerializer, LoginSerializer,HistoricoTesouroSerializer
import requests
from rest_framework.decorators import action
from .models import HistoricoTesouro
from rest_framework import viewsets


def index(request):
    now = datetime.now()
    html = f'''
    <html>
        <body>
            <h1>Hello from Vercel!</h1>
            <p>The current time is { now }.</p>
        </body>
    </html>
    '''
    return HttpResponse(html)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')


@extend_schema(request=LoginSerializer, responses=UserSerializer)
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def api_login(request):
    # valida com serializer para o Swagger
    from django.contrib.auth import authenticate
    login_serializer = LoginSerializer(data=request.data)
    login_serializer.is_valid(raise_exception=True)
    username = login_serializer.validated_data['username']
    password = login_serializer.validated_data['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)  # cria sessão
        # obtiene token CSRF
        from django.middleware.csrf import get_token
        token = get_token(request)
        user_serial = UserSerializer(user)
        data = user_serial.data
        # include admin flag
        data['is_admin'] = user.is_staff or user.is_superuser
        data['csrf_token'] = token
        return Response(data)
    return Response({'detail': 'Invalid credentials'}, status=400)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tesouro_time_series(request):
    ''' Exemplo de uso:
        GET /api/tesouro-series/?starting_date=01/01/2025
        GET /api/tesouro-series/?starting_date=2025-01-01'''
    # Parâmetro opcional de data de início
    starting_date_str = request.GET.get('starting_date')
    starting_date = None
    
    if starting_date_str:
        try:
            # Suporta formatos DD/MM/YYYY e YYYY-MM-DD
            if '/' in starting_date_str:
                starting_date = datetime.strptime(starting_date_str, '%d/%m/%Y')
            else:
                starting_date = datetime.strptime(starting_date_str, '%Y-%m-%d')
        except ValueError:
            return Response({'error': 'Formato de data inválido. Use DD/MM/YYYY ou YYYY-MM-DD'}, status=400)
    
    historico_data = HistoricoTesouro.objects.all().order_by('data_captura')
    
    # Filtrar por data de início se fornecida
    if starting_date:
        historico_data = historico_data.filter(data_captura__gte=starting_date)
    
    series = {}

    for record in historico_data:
        payload = record.payload_cru
        timestamp = record.data_captura.isoformat()  # Para JSON serializable

        # Processar TesouroLegado e Tesouro24x7
        for category in ['TesouroLegado', 'Tesouro24x7']:
            if payload.get(category):
                for titulo in payload[category]:
                    key = titulo['isinCode']
                    name = titulo['treasuryBondName']
                    value = titulo['unitaryInvestmentValue']

                    if key not in series:
                        series[key] = {
                            'label': name,
                            'data': []
                        }

                    series[key]['data'].append({
                        'x': timestamp,
                        'y': value
                    })

    # Converter para lista
    chart_data = list(series.values())
    return Response({'series': chart_data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def titulo_time_series(request):
    ''' Exemplo de uso:
        GET /api/titulo-series/?name=Prefixado%202035&starting_date=2025-01-01
        GET /api/tesouro-series/  # Sem data, processa tudo'''
    
    titulo_name = request.GET.get('name')
    if not titulo_name:
        return Response({'error': 'Nome do título é obrigatório'}, status=400)
    
    # Parâmetro opcional de data de início
    starting_date_str = request.GET.get('starting_date')
    starting_date = None
    
    if starting_date_str:
        try:
            # Suporta formatos DD/MM/YYYY e YYYY-MM-DD
            if '/' in starting_date_str:
                starting_date = datetime.strptime(starting_date_str, '%d/%m/%Y')
            else:
                starting_date = datetime.strptime(starting_date_str, '%Y-%m-%d')
        except ValueError:
            return Response({'error': 'Formato de data inválido. Use DD/MM/YYYY ou YYYY-MM-DD'}, status=400)
    
    historico_data = HistoricoTesouro.objects.all().order_by('data_captura')
    
    # Filtrar por data de início se fornecida
    if starting_date:
        historico_data = historico_data.filter(data_captura__gte=starting_date)
    
    data_points = []

    for record in historico_data:
        payload = record.payload_cru
        timestamp = record.data_captura.isoformat()

        for category in ['TesouroLegado', 'Tesouro24x7']:
            if payload.get(category):
                for titulo in payload[category]:
                    if titulo['treasuryBondName'] == titulo_name:
                        data_points.append({
                            'x': timestamp,
                            'y': titulo['unitaryInvestmentValue']
                        })
                        break  # Assumindo que o nome é único

    return Response({'label': titulo_name, 'data': data_points})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """API que retorna estatísticas gerais dos títulos do Tesouro"""
    ultimo = HistoricoTesouro.objects.order_by('-data_captura').first()
    if not ultimo:
        return Response({'error': 'Nenhum dado disponível'}, status=400)
    
    payload = ultimo.payload_cru
    titulos_list = []
    rentabilidade_count = {}
    categoria_count = {'TesouroLegado': 0, 'Tesouro24x7': 0}
    
    # Processar todos os títulos
    for category in ['TesouroLegado', 'Tesouro24x7']:
        if payload.get(category):
            categoria_count[category] = len(payload[category])
            for titulo in payload[category]:
                value = titulo.get('unitaryInvestmentValue', 0)
                profitability = titulo.get('investmentProfitabilityIndexerName', 'Outros')
                
                titulos_list.append({
                    'name': titulo['treasuryBondName'],
                    'value': value,
                    'profitability': profitability,
                    'category': category
                })
                
                # Contar por tipo de rentabilidade
                if profitability not in rentabilidade_count:
                    rentabilidade_count[profitability] = 0
                rentabilidade_count[profitability] += 1
    
    # Calcular estatísticas
    valores = [t['value'] for t in titulos_list]
    total_titulos = len(titulos_list)
    valor_medio = sum(valores) / len(valores) if valores else 0
    valor_minimo = min(valores) if valores else 0
    valor_maximo = max(valores) if valores else 0
    
    # Top 10 títulos por valor
    top_10 = sorted(titulos_list, key=lambda x: x['value'], reverse=True)[:10]
    
    return Response({
        'total_titulos': total_titulos,
        'valor_medio': round(valor_medio, 2),
        'valor_minimo': round(valor_minimo, 2),
        'valor_maximo': round(valor_maximo, 2),
        'por_categoria': categoria_count,
        'por_rentabilidade': rentabilidade_count,
        'top_10_titulos': top_10,
        'data_captura': ultimo.data_captura.isoformat()
    })


