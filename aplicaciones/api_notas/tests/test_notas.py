import pytest
from django.urls import reverse
from django.db.models import Q
from rest_framework.test import APIClient
from aplicaciones.notas.models import Nota
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_crear_nota():
    cliente = APIClient()

    user = User.objects.create_user(username='usuario1', password='nomelase')

    login_response = cliente.post(reverse('token_obtain_pair') , {
        'username': 'usuario1',
        'password': 'nomelase'
    })

    assert login_response.status_code == 200

    token = login_response.data['access']

    cliente.credentials(HTTP_AUTHORIZATION = f'Bearer {token}')

    url_crear = reverse('nota-list')

    response = cliente.post(url_crear, {
        'titulo': 'prueba',
        'contenido': 'jijijija',
        "categoria": "personal"
    }, format='json' )

    assert response.status_code == 201


@pytest.mark.django_db
def test_modificar_nota():
    cliente = APIClient()

    user = User.objects.create_user(username='usuario1', password='nomelase')

    login_response = cliente.post(reverse('token_obtain_pair'), {
        'username': 'usuario1',
        'password': 'nomelase'
    })

    assert login_response.status_code == 200
    token = login_response.data['access']

    cliente.credentials(HTTP_AUTHORIZATION = f'Bearer {token}')

    url_crear = reverse('nota-list')

    response = cliente.post(url_crear, {
        'titulo': 'nuevotitulp',
        'contenido': 'jijijija',
        'categoria': 'trabajo'
    }, format='json')

    assert response.status_code == 201

    nota_id = response.data['id']

    url_modificar = reverse('nota-detail', kwargs={'pk': nota_id})

    response = cliente.patch(url_modificar, {
        'titulo': 'Nuevo Titulo'
    }, format='json')

    assert response.status_code == 200
    nota = Nota.objects.get(id=nota_id)
    assert nota.titulo == 'Nuevo Titulo'


@pytest.mark.django_db
def test_eliminiar_nota():
    cliente = APIClient()

    user = User.objects.create_user(username='usuario1', 
                                    password='nomelase',
                                    nombre='Juan',
                                    apellidoP='Lopez',
                                    apellidoM='Perez')

    usuario_id = user.id
    
    login_response = cliente.post(reverse('token_obtain_pair') , {
        'username': 'usuario1',
        'password': 'nomelase'
    }, format='json')
    
    assert login_response.status_code == 200

    token = login_response.data['access']

    cliente.credentials(HTTP_AUTHORIZATION = f'Bearer {token}')

    response = cliente.post(reverse('nota-list'), {
        'titulo': 'titulo 1',
        'contenido': 'Halo 3',
        'categoria': 'trabajo'
    }, format='json')

    nota_id = response.data['id']
    assert response.status_code == 201

    nota = Nota.objects.get(usuario=usuario_id, id=nota_id)
    
    nota.activo = False
    nota.save()
    assert Nota.objects.get(usuario=usuario_id, id=nota_id).activo == False


@pytest.mark.django_db
def test_activar_nota():
    cliente = APIClient()

    user = User.objects.create_user(username='usuario1', 
                                    password='nomelase',
                                    nombre='Juan',
                                    apellidoP='Lopez',
                                    apellidoM='Perez')

    usuario_id = user.id

    response = cliente.post(reverse('token_obtain_pair') , {
        'username': 'usuario1',
        'password': 'nomelase'
    }, format='json')

    assert response.status_code == 200

    token = response.data['access']

    cliente.credentials(HTTP_AUTHORIZATION = f'Bearer {token}')

    response = cliente.post(reverse('nota-list'), {
        'titulo': 'titulo 1',
        'contenido': 'Halo 3',
        'categoria': 'trabajo'
    }, format='json')

    assert response.status_code == 201
    nota_id = response.data['id']

    nota = Nota.objects.get(id=nota_id, usuario=usuario_id)
    nota.activo = True
    nota.save()
    assert nota.activo  == True


@pytest.mark.django_db
def test_error_modificar_nota():
    #Test para probar si un usuario por alguna razon intenta modificar la nota de otro usuario

    cliente = APIClient()

    user1 = User.objects.create_user(username='usuario1', password='123')
    user2 = User.objects.create_user(username='usuario2', password='456')                            
                            
    nota = Nota.objects.create(titulo='Titulo usuario 1', contenido='jijijija', categoria='otro', usuario=user1)

    cliente.force_authenticate(user=user2)

    response = cliente.patch(reverse('nota-detail', kwargs={'pk': nota.id},), {
        'titulo':'Titulo Usuario 2',
        'contenido': 'HOLA MUNDO',
        'categoria': 'trabajo'
    }, format='json')

    assert response.status_code == 404

@pytest.mark.django_db
def test_error_eliminar_nota():
    #Test de error al intentar eliminar una nota ajena lo cual ni deberia pasar
    cliente = APIClient()

    user1 = User.objects.create_user(username='usuario1', password='123')
    user2 = User.objects.create_user(username='usuario2', password='456') 

    nota = Nota.objects.create(titulo='Titulo usuario 1', contenido='jijijija', categoria='otro', usuario=user1)

    cliente.force_authenticate(user=user2)

    response = cliente.delete(reverse('nota-detail', kwargs={'pk': nota.id}))

    assert response.status_code == 404


@pytest.mark.django_db
def test_nota_sin_autorizacion():
    cliente = APIClient()
    response = cliente.post(reverse('nota-list'), {
        'titulo':'prueba',
        'contenido': 'contenido',
        'categoria': 'otro'
    }, format='json')
    assert response.status_code == 401


@pytest.mark.django_db
def test_listar_obtener_notas_usuario():
    cliente = APIClient()
    user1 = User.objects.create_user(username='user1', password='123')
    user2 = User.objects.create_user(username='user2', password='456')

    Nota.objects.create(titulo='Nota 1', contenido='abcd', categoria='otro', usuario=user1)
    Nota.objects.create(titulo='Nota 2', contenido='efg', categoria='otro', usuario=user2)

    cliente.force_authenticate(user=user1)
    response = cliente.get(reverse('nota-list'))

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['titulo'] == 'Nota 1'


@pytest.mark.django_db
def test_titulo_vacio():
    cliente = APIClient()

    user = User.objects.create_user(username='usuario1', password='123')

    cliente.force_authenticate(user=user)

    response = cliente.post(reverse('nota-list'), {
        'titulo': '',
        'contenido': 'contenido 123',
        'categoria': 'personal'  
    }, format='json')

    assert response.status_code == 400
    assert 'titulo' in response.data

@pytest.mark.django_db
def test_contenido_vacio():
    cliente = APIClient()

    user = User.objects.create_user(username='usuario1', password='123')

    cliente.force_authenticate(user=user)

    response = cliente.post(reverse('nota-list'), {
        'titulo': 'titulo 123',
        'contenido': '',
        'categoria': 'personal'  
    }, format='json')

    assert response.status_code == 400
    assert 'contenido' in response.data

@pytest.mark.django_db
def test_categoria_invalida():
    cliente = APIClient()
    
    user = User.objects.create_user(username='usuario1', password='pswd123')

    cliente.force_authenticate(user=user)

    response = cliente.post(reverse('nota-list'), {
        'titulo': 'titulo123',
        'contenido': 'contenido123',
        'categoria': 'inventada'
    }, format='json')

    assert response.status_code == 400
    assert 'categoria' in response.data


@pytest.mark.django_db
def test_categoria_vacio():
    cliente = APIClient()

    user = User.objects.create_user(username='usuario1', password='123')

    cliente.force_authenticate(user=user)

    response = cliente.post(reverse('nota-list'), {
        'titulo': 'titulo 123',
        'contenido': 'contenido 123',
        'categoria': ''  
    }, format='json')

    assert response.status_code == 400
    assert 'categoria' in response.data



@pytest.mark.django_db
def test_buscar_texto():
    cliente = APIClient()
    
    user = User.objects.create_user(username='usuario1', password='pswd123')

    nota1 = Nota.objects.create(titulo='t1', contenido='c1 Halo', categoria='trabajo', usuario=user)
    nota2 = Nota.objects.create(titulo='Halo', contenido='c2', categoria='trabajo', usuario=user)
    nota3 = Nota.objects.create(titulo='t3', contenido='c3', categoria='trabajo', usuario=user)

    search = 'hal'

    cantidad = Nota.objects.filter(
        usuario=user
    ).filter(
        Q(titulo__icontains=search) | Q(contenido__icontains=search)
    ).count()

    assert cantidad == 2




