import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_crear_usuario():
    cliente = APIClient()
    response = cliente.post(reverse('usuario-list'), {
        'username': 'usuario1',
        'password': 'nomelase',
        'nombre': 'fulano',
        'apellidoP': 'detal',
        'apellidoM': 'lopez' 
    })

    assert response.status_code == 201
    assert User.objects.filter(username='usuario1').exists()

@pytest.mark.django_db
def test_login():
    cliente = APIClient()

    response = cliente.post(reverse('usuario-list'), {
        'username': 'usuario1',
        'password': 'nomelase',
        'nombre': 'fulano',
        'apellidoP': 'detal',
        'apellidoM': 'lopez' 
    })

    assert response.status_code == 201

    login_response = cliente.post(reverse('token_obtain_pair'), {
        'username': 'usuario1',
        'password': 'nomelase'
    })

    assert login_response.status_code == 200
    assert 'access' in login_response.data

    
@pytest.mark.django_db
def test_error_crear_usuario_duplicado():
    cliente = APIClient()

    User.objects.create_user(username='usuario2', password='nimelase')
    
    response = cliente.post(reverse('usuario-list'), {
        'username': 'usuario2',
        'password': 'aaaa',
        'nombre': 'Carlos',
        'apellidoP': 'Lopez',
        'apellidoM': 'Garcia',
        'email': 'carlos@example.com'
    }, format='json')

    assert response.status_code == 400


@pytest.mark.django_db
def test_error_get():
    #No esta permitido el get en el viewset, tienes que usar Perfil

    cliente = APIClient()
    
    user = User.objects.create_user(username='usuario1', password='pswd123')
    cliente.force_authenticate(user=user)

    response = cliente.get(reverse('usuario-list'))

    assert response.status_code == 405

@pytest.mark.django_db
def test_perfil_get():
    #El get se encuentra en Perfil

    cliente = APIClient()

    user = User.objects.create_user(username='usuario1', password='pswd123')
    cliente.force_authenticate(user=user)

    response = cliente.get(reverse('usuario-perfil') )

    assert response.status_code == 200
    assert response.data['username'] == 'usuario1'


@pytest.mark.django_db
def test_modificar_usuario_perfil():
    #Se modifica el usuario desde perfil
    
    cliente = APIClient()

    response = cliente.post(reverse('usuario-list'), {
        'username': 'usuario1',
        'password': 'nomelase',
        'nombre': 'fulano',
        'apellidoP': 'detal',
        'apellidoM': 'lopez' 
    }, format='json')
    assert response.status_code == 201

    response = cliente.post(reverse('token_obtain_pair'), {
        'username': 'usuario1',
        'password': 'nomelase'
    }, format='json')
    assert response.status_code == 200

    token = response.data['access']
    cliente.credentials(HTTP_AUTHORIZATION = f'Bearer {token}')

    response = cliente.patch(reverse('usuario-perfil'), {
        'nombre': 'mengano'
    })

    assert response.status_code == 200
    assert response.data['nombre'] == 'mengano'


@pytest.mark.django_db
def test_error_crear_usuario_username_repetido():
    cliente = APIClient()

    user1 = User.objects.create_user(username='usuario1', password='pswd123', nombre='nombre1', apellidoP='ap1', apellidoM='am1')
    #user1 = User.objects.create_user(username='usuario2', password='pswd123', nombre='nombre2', apellidoP='ap2', apellidoM='am2')

    response = cliente.post(reverse('usuario-list'), {
        'username': 'usuario1',
        'nombre': 'n2',
        'password': 'a123',
        'apellidoP': 'ap2',
        'apellidoM': 'am2'
    })

    assert response.status_code == 400


@pytest.mark.django_db
def test_error_modficiar_username_repetido():
    cliente = APIClient()

    user1 = User.objects.create_user(username='usuario1', password='pswd123', nombre='nombre1', apellidoP='ap1', apellidoM='am1')
    user2 = User.objects.create_user(username='usuario2', password='pswd123', nombre='nombre2', apellidoP='ap2', apellidoM='am2')

    cliente.force_authenticate(user=user2)

    response = cliente.patch(reverse('usuario-perfil'), {
        'username': 'usuario1'
    }, format='json')

    assert response.status_code == 400
    user2.refresh_from_db()
    assert user2.username == 'usuario2'



@pytest.mark.django_db
def test_usuario_no_puede_modificar_otro_usuario():
    #Tecnicamente esta prueba esta de mas a que uso request.user en "Perfil" de usuario
    cliente = APIClient()

    user1 = User.objects.create_user(username='usuario1', password='1234', nombre='Nombre1')
    user2 = User.objects.create_user(username='usuario2', password='5678', nombre='Nombre2')

    cliente.force_authenticate(user=user1)

    response = cliente.patch(reverse('usuario-perfil'), {
        'id': user2.id,
        'username': 'nuevo_username',
        'nombre': 'Hack'
    })

    user1.refresh_from_db()
    user2.refresh_from_db()
    assert response.status_code == 200
    assert user1.nombre == 'Hack'
    assert user2.username == 'usuario2' 
