from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    nombre = models.CharField(verbose_name='Nombre', null=False, blank=False, max_length=25)
    apellidoP = models.CharField(verbose_name='Apellido paterno', null=False, blank=False, max_length=20)
    apellidoM = models.CharField(verbose_name='Apellido materno', null=False, blank=False, max_length=20)

    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f'{self.username}'



