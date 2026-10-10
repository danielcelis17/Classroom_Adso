# Fase 3 · JWT Authentication with Django REST Framework

Guía: [`insumos/2-JWT Authentication with Django REST Framework.docx`](../insumos/2-JWT%20Authentication%20with%20Django%20REST%20Framework.docx)

Parte de la [fase 1](../fase-1-api-rest-django-mysql/) y protege el API de la base `ventas` con tokens JWT (Simple JWT). Además de `cliente`, expone `comercial` y `pedido`, como pide la guía.

## Pasos de la guía y dónde quedaron

| Paso | Qué pide la guía | Dónde está |
|------|------------------|------------|
| 3 | Instalar `djangorestframework_simplejwt` | `requirements.txt` |
| 5 | Agregar `rest_framework_simplejwt` a `INSTALLED_APPS` | `server/settings.py` |
| 6–7 | `timedelta`, `REST_FRAMEWORK` y `SIMPLE_JWT` | `server/settings.py` |
| 8–9 | Endpoints `api/token/` y `api/token/refresh/`, e `include('api.urls')` | `server/urls.py`, `api/urls.py` |
| 10–11 | `IsAuthenticated` y `JWTAuthentication` en `ClienteViewSet`, `ComercialViewSet` y `PedidoViewSet` | `api/views.py` |
| 12 | `python manage.py migrate` | Se ejecuta solo al arrancar el contenedor |
| 13 | `python manage.py createsuperuser` | Ver "Cómo ejecutarlo" |
| 14 | Probar con Bruno | `bruno/` |

Diferencias con la guía:

- `SIMPLE_JWT` no incluye `SLIDING_TOKEN_*_LATE_USER`, porque Simple JWT no las reconoce. Se agregó `REFRESH_TOKEN_LIFETIME` (1 día).
- Las rutas van sin barra final (`/api/cliente`) para conservar la ruta de la fase 1.

## Endpoints

| Método | Ruta                  | Descripción |
|--------|-----------------------|-------------|
| POST   | `/api/token/`         | Recibe `username` y `password`; devuelve `access` y `refresh` |
| POST   | `/api/token/refresh/` | Recibe `refresh`; devuelve un `access` nuevo |
| GET, POST | `/api/cliente`, `/api/comercial`, `/api/pedido` | Listar y crear |
| GET, PUT, PATCH, DELETE | `/api/cliente/<id>`, `/api/comercial/<id>`, `/api/pedido/<id>` | Consultar, editar y borrar |

Todos menos los de token exigen `Authorization: Bearer <access>`; sin él responden `401`. El token de acceso dura 60 minutos.

## Cómo ejecutarlo

### Como en la guía (WampServer y entorno virtual)

1. Inicia WampServer e importa `db/ventas_db.sql` en MySQL (usuario `root`, sin contraseña).
2. Desde esta carpeta, en CMD o PowerShell:

   ```bash
   py -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   py manage.py migrate
   py manage.py createsuperuser
   py manage.py runserver
   ```

Sin archivo `.env`, el proyecto usa la misma conexión de la guía: base `ventas`, usuario `root`, sin contraseña, `localhost:3306`.

### Con Docker

Desde esta carpeta:

```bash
cp .env.example .env
docker compose up --build
docker compose exec web python manage.py createsuperuser
```

## Probar con Bruno

1. Abre la carpeta `bruno/` y selecciona el entorno `local`.
2. Escribe el `username` y el `password` del superusuario en el entorno.
3. Ejecuta **Obtener token**: el token se guarda solo y las demás peticiones lo usan.
4. Cuando venza, ejecuta **Refrescar token**.
