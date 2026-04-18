# example/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from example.views import  index, login_view, logout_view, user_profile, api_login, tesouro_time_series, titulo_time_series, dashboard_stats
from .viewsets import UserViewSet, HistoricoTesouroViewSet

router = DefaultRouter()

#viewsets
router.register(r'users', UserViewSet)
router.register(r'historico-tesouro', HistoricoTesouroViewSet, basename='historico-tesouro')


urlpatterns = [
    path('', index, name='index'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('api/user/', user_profile, name='user_profile'),
    path('api/login/', api_login, name='api_login'),
    path('api/tesouro-series/', tesouro_time_series, name='tesouro_series'),
    path('api/titulo-series/', titulo_time_series, name='titulo_series'),
    path('api/dashboard-stats/', dashboard_stats, name='dashboard_stats'),
    
] + router.urls