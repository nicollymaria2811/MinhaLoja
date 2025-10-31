# loja/admin.py
from django.contrib import admin
from .models import Produto

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'quantidade', 'disponivel', 'imagem')
    list_filter = ('disponivel',)
    search_fields = ('nome',)
    list_editable = ('preco', 'quantidade', 'disponivel')
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'preco', 'quantidade')
        }),
        ('Disponibilidade', {
            'fields': ('disponivel',)
        }),
        ('Imagem', {
            'fields': ('imagem',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request)