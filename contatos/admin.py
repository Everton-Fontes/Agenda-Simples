from django.contrib import admin
from .models import Contato, Categoria


# Register your models here.


class ContatoAdmin(admin.ModelAdmin):
    list_display = ("nome", 'sobrenome', 'telefone', 'descricao', 'mostrar')
    list_display_links = ("nome", 'sobrenome')
    search_fields = ('nome', 'telefone', 'email')
    list_per_page: int = 10
    list_editable = ('mostrar',)


admin.site.register(Contato, ContatoAdmin)
admin.site.register(Categoria)
