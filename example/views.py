# example/views.py
from datetime import datetime
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import permissions
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .serializers import UserSerializer, LoginSerializer

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