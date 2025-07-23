from django.contrib.auth import get_user_model
from rest_framework import serializers
from aplicaciones.notas.models import Nota

User = get_user_model()

class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    #username = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['url', 'username','password','nombre', 'apellidoP', 'apellidoM', 'email']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = self.Meta.model(**validated_data)
        user.set_password(password)  
        user.save()
        return user

    def update(self, instance, validated_data):
        validated_data.pop('username', None)
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)  
        instance.save()
        return instance


class NotaSerializer(serializers.HyperlinkedModelSerializer):
    usuario = serializers.ReadOnlyField(source='usuario.username')  
    fecha_creacion = serializers.ReadOnlyField()

    class Meta:
        model = Nota
        fields = ['url','id', 'usuario', 'titulo', 'contenido', 'categoria', 'fecha_creacion', 'activo']
