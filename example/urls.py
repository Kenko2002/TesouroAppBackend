# example/urls.py
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework.routers import DefaultRouter
from example.views import index, login_view, logout_view, user_profile
from .viewsets import UserViewSet
from .views import api_login

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('api/myuser/', user_profile, name='user_profile'),    path('api/login/', api_login, name='api_login'),] + router.urls