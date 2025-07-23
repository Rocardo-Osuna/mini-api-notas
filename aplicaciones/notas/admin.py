from django.contrib import admin
from .models import Nota 

@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):

    list_display = ('usuario', 'titulo', 'contenido', 'categoria', 'fecha_creacion', 'activo')
    search_fields = ('usuario__username',)
    list_filter = ('categoria',)
    readonly_fields = ('fecha_creacion',)
