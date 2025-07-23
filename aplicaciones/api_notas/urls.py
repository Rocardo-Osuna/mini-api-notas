from django.urls import path, include
from. import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'usuarios', views.UsuarioViewSet, basename="usuario")
router.register(r'notas', views.NotaViewSet, basename='nota')

urlpatterns = [
    path('', include(router.urls)),
]