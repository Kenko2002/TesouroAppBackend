# example/views.py
from datetime import datetime
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserSerializer

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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def api_login(request):
    # espera campos 'username' e 'password'
    username = request.data.get('username')
    password = request.data.get('password')
    from django.contrib.auth import authenticate
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)  # cria sessão
        # obtiene token CSRF
        from django.middleware.csrf import get_token
        token = get_token(request)
        serializer = UserSerializer(user)
        data = serializer.data
        data['csrf_token'] = token
        return Response(data)
    return Response({'detail': 'Invalid credentials'}, status=400)