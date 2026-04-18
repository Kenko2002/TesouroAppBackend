from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Formulario

@admin.register(User)
class MyUserAdmin(UserAdmin):
    # Adiciona o campo 'bio' nos formulários de edição do Admin
    # O fieldsets controla a organização da página de edição
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {'fields': ('bio',)}),
    )
    
    # Adiciona o campo 'bio' no formulário de criação (opcional)
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Adicionais', {'fields': ('bio',)}),
    )

@admin.register(Formulario)
class FormularioAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'descricao')
    readonly_fields = ('created_at',)
    search_fields = ('user__username', 'descricao')

