from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, HistoricoTesouro

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



@admin.register(HistoricoTesouro)
class HistoricoTesouroAdmin(admin.ModelAdmin):
    list_display = ('data_captura',)
    readonly_fields = ('data_captura',)
    search_fields = ('payload_cru','data_captura')