from django.db import models
from aplicaciones.usuarios.models import Usuario

class Nota(models.Model):

    CATEGORIA = (
        ('personal','Personal'),
        ('trabajo', 'Trabajo'),
        ('estudio', 'Estudio'),
        ('ocio', 'Ocio'),
        ('otro', 'Otro'),
    )

    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    titulo = models.CharField(max_length=100, blank=False, null=False)
    contenido = models.TextField()
    categoria = models.CharField(choices=CATEGORIA, blank=False, null=False, max_length=20, default='otro')
    fecha_creacion = models.DateField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'notas'
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'
        
    def __str__(self):
        return self.titulo
