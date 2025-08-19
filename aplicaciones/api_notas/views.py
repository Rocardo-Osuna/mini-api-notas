from django.shortcuts import render
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, NotaSerializer, CambiarUsernameSerializer, CambiarPasswordSerializer
from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from aplicaciones.notas.models import Nota




class UsuarioViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get', 'put', 'patch'], permission_classes=[IsAuthenticated])
    def perfil(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        elif request.method in ['PUT', 'PATCH']:
            serializer = self.get_serializer(request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def cambiar_username(self, request):
        serializer = CambiarUsernameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request.user.username = serializer.validated_data['nuevo_username']
        request.user.save()

        return Response({'status': 'Username actualizado correctamente'}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def cambiar_password(self, request):
        serializer = CambiarPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        nuevo_password = serializer.validated_data['nuevo_password1']
        request.user.set_password(nuevo_password)
        request.user.save()

        return Response({'status': 'Contraseña actualizada correctamente'}, status=status.HTTP_200_OK)

        
    

class NotaViewSet(viewsets.ModelViewSet):
    serializer_class = NotaSerializer

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['titulo', 'contenido']
    ordering_fields = ['fecha_creacion']  
    ordering = ['-fecha_creacion']  

    def get_queryset(self):
        usuario = self.request.user
        categoria = self.request.GET.get('categoria')
        borrados = self.request.GET.get('borrados', 'false').lower()  

        if borrados == 'true':
            q = Nota.objects.filter(usuario=usuario, activo=False)
        else:
            q = Nota.objects.filter(usuario=usuario, activo=True)

        if categoria:
            q = q.filter(categoria=categoria)

        return q

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    def destroy(self, request, pk=None):
        nota = self.get_object()

        if nota.usuario != request.user:
            return Response({'detail': 'No tienes permiso para eliminar esta nota'}, status=status.HTTP_403_FORBIDDEN)

        nota.activo = False
        nota.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['post'])
    def reactivar(self, request, pk=None):

        try:
            nota = Nota.objects.get(pk=pk, usuario=request.user)
        except Nota.DoesNotExist:
            return Response({'detail': 'Nota no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        
        if nota.usuario != request.user:
            return Response({'detail': 'Error de notas'}, status=status.HTTP_403_FORBIDDEN)
        
        if nota.activo:
            return Response({'detail': 'La nota ya esta activa'},status=status.HTTP_400_BAD_REQUEST)
        
        nota.activo = True
        nota.save()
        serializer = self.get_serializer(nota)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        usuario = self.request.user
        notas = Nota.objects.filter(usuario=usuario)

        categorias = {}

        for nota in notas:
            if nota.categoria in categorias:
                categorias[nota.categoria] +=1 
            else:
                categorias[nota.categoria] = 1

        total = notas.count()
        activas = notas.filter(activo=True).count()
        borradas = notas.filter(activo=False).count()

        estadisticas = {
            'total': total,
            'categorias': categorias,
            'activas': activas,
            'borradas': borradas
        }

        return Response(estadisticas)
