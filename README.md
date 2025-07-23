# Mini API de Notas

Como método de aprendizaje, realicé esta mini API para una aplicación de notas.  
Es bastante simple, pero el objetivo principal fue repasar varias tecnologías útiles en el desarrollo backend con Django

Tecnologías utilizadas:

- Django
- Django REST Framework (DRF)
- JWT (JSON Web Tokens)
- Pytest
- drf-spectacular (para documentación automática)


## Django

Implementé una estructura mínima con los dos modelos esenciales para una app de notas

- Un modelo de usuario personalizado
- Un modelo de nota

Ambos modelos están registrados en el panel de administración (`admin`) de Django


## Django REST Framework

Utilicé viewsets para manejar los endpoints

### Usuarios

- `POST /api/usuarios/`  
  Crear un usuario. Requiere: `username`, `nombre`, `apellidoP`, `apellidoM`, `email`

- `GET /api/usuarios/perfil/`  
  Obtener información del usuario autenticado

- `PUT /api/usuarios/perfil/`  
  Actualizar todo el perfil del usuario autenticado

- `PATCH /api/usuarios/perfil/`  
  Modificar parcialmente el perfil

Agregare a futuro una opcion exclusiva para editar nombre y contraseña, actualmente se puede hacer con path y put


### Notas

- `GET /api/notas/`  
  Listar las notas activas del usuario.  
  Parámetros opcionales:
  - `search`: busca texto en titulo y contenido de la nota
  - `categoria`: filtra por categoría
  - `borrados`: `true` para ver notas eliminadas lógicamente

- `DELETE /api/notas/`  
  Elimina lógicamente una nota. Se necesita el ID de la nota

- `POST /api/notas/reactivar/`  
  Reactiva una nota borrada (requiere ID)

- `GET /api/notas/estadisticas/`  
  Devuelve estadísticas sobre las notas del usuario y sus categorías


## Pytest

Incluye pruebas automatizadas con **Pytest**, ubicadas en la carpeta del proyecto de api_notas

