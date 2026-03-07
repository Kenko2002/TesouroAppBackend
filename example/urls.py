# example/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from example.views import index, login_view, logout_view, user_profile, api_login
from .viewsets import UserViewSet, FormularioViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'formularios', FormularioViewSet)

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('api/user/', user_profile, name='user_profile'),
    path('api/login/', api_login, name='api_login'),
] + router.urls