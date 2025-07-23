from django.contrib import admin
from .models import Usuario
from django.contrib.auth.admin import UserAdmin
from .forms import UsuarioCambioForm, UsuarioCreacionForm


@admin.register(Usuario)
class Admin(UserAdmin):
    add_form = UsuarioCreacionForm
    form = UsuarioCambioForm
    #model = Usuario

    list_display = ('username', 'nombre', 'apellidoP', 'apellidoM', 'is_active', 'is_staff','email')
    search_fields = ('username', 'nombre', 'apellidoP', 'apellidoM','email')
    list_filter = ('is_active', 'is_staff')
    ordering = ['date_joined']

    fieldsets = (
        (' ', {'fields': ('username', 'password')}),
        ('Informacion Personal', {'fields': ('nombre', 'apellidoP', 'apellidoM','email')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('fechas importantes', {
            'classes': ('collapse',),
            'fields': ('last_login', 'date_joined')}
            ),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2','nombre', 'apellidoP', 'apellidoM','email')
        }),
    )



