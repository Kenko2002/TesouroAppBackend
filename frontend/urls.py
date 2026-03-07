from django.urls import path
from .views import login_view, logout_view, home_admin, cadastrar_formulario

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home_admin/', home_admin, name='home_admin'),
    path('cadastrar_formulario/', cadastrar_formulario, name='cadastrar_formulario'),
]