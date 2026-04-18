from django.urls import path
from .views import login_view, logout_view, home_user, home_admin, titles_visualization

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home_user/', home_user, name='home_user'),
    path('titles_visualization/', titles_visualization, name='titles_visualization'),
    path('home_admin/', home_admin, name='home_admin'),
]