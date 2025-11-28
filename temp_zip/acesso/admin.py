from django.contrib import admin
from .models import Modulo, PermissaoModulo

@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')
    search_fields = ('nome',)

@admin.register(PermissaoModulo)
class PermissaoModuloAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'modulo')
    list_filter = ('modulo',)
    search_fields = ('usuario__username', 'modulo__nome')
    raw_id_fields = ('usuario', 'modulo')
