# Fase 4 · Implementación JWT Authentication con Django REST Framework en la base de datos Tienda

Guía base: [`insumos/2-JWT Authentication with Django REST Framework.docx`](../insumos/2-JWT%20Authentication%20with%20Django%20REST%20Framework.docx)
Base de datos: [`insumos/tienda_db.sql`](../insumos/tienda_db.sql) (copiada en `db/tienda_db.sql`)

Aplica los mismos pasos de la [fase 3](../fase-3-jwt-authentication/) a la base `tienda`: la app `api` expone clientes, productos, facturas y detalle de facturas, todo protegido con JWT.

## Pasos de la guía y dónde quedaron

| Paso | Qué pide la guía | Dónde está |
|------|------------------|------------|
| 3 | Instalar `djangorestframework_simplejwt` | `requirements.txt` |
| 5–7 | `rest_framework_simplejwt` en `INSTALLED_APPS`, `REST_FRAMEWORK` y `SIMPLE_JWT` | `server/settings.py` |
| 8–9 | Endpoints `api/token/` y `api/token/refresh/`, e `include('api.urls')` | `server/urls.py`, `api/urls.py` |
| 10–11 | `IsAuthenticated` y `JWTAuthentication` en cada ViewSet | `api/views.py` |
| 12 | `python manage.py migrate` | Se ejecuta solo al arrancar el contenedor |
| 13 | `python manage.py createsuperuser` | Ver "Cómo ejecutarlo" |
| 14 | Probar con Bruno | `bruno/` |

Los modelos (`api/models.py`) corresponden a las tablas de `tienda_db.sql` y usan `managed = False`: las tablas las crea el script, no Django.

## Endpoints

| Método | Ruta                  | Descripción |
|--------|-----------------------|-------------|
| POST   | `/api/token/`         | Recibe `username` y `password`; devuelve `access` y `refresh` |
| POST   | `/api/token/refresh/` | Recibe `refresh`; devuelve un `access` nuevo |
| GET, POST | `/api/clientes`, `/api/productos`, `/api/facturas`, `/api/detalle-facturas` | Listar y crear |
| GET, PUT, PATCH, DELETE | Las mismas rutas con `/<id>` | Consultar, editar y borrar |

- Todos menos los de token exigen `Authorization: Bearer <access>`; sin él responden `401`.
- Cada factura muestra sus líneas en el campo `detalles`. Al borrar una factura se borran sus líneas.
- No se puede borrar un cliente o un producto que aparece en una factura: la API responde `409`.

## Cómo ejecutarlo

### Como en la guía (WampServer y entorno virtual)

1. Inicia WampServer e importa `db/tienda_db.sql` en MySQL (usuario `root`, sin contraseña).
2. Desde esta carpeta, en CMD o PowerShell:

   ```bash
   py -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   py manage.py migrate
   py manage.py createsuperuser
   py manage.py runserver
   ```

Sin archivo `.env`, el proyecto se conecta a la base `tienda` con usuario `root`, sin contraseña, en `localhost:3306`.

### Con Docker

Desde esta carpeta:

```bash
cp .env.example .env
docker compose up --build
docker compose exec web python manage.py createsuperuser
```

La primera vez MySQL ejecuta `db/tienda_db.sql`; la base empieza vacía.

## Probar con Bruno

1. Abre la carpeta `bruno/` y selecciona el entorno `local`.
2. Escribe el `username` y el `password` del superusuario en el entorno.
3. Ejecuta **Obtener token**.
4. Ejecuta en orden: crear cliente, crear producto, crear factura y agregar detalle a factura.
