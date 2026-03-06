from django.contrib import admin
from .models import User, Formulario

# Register your models here.
admin.site.register(User)

@admin.register(Formulario)
class FormularioAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'descricao')
    readonly_fields = ('created_at',)
    search_fields = ('user__username', 'descricao')

