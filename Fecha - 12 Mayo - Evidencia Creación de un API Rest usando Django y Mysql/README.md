# Fase 1 · Creación de un API Rest usando Django y MySQL

Guía: [`insumos/1-API Rest Python Django.docx`](../insumos/1-API%20Rest%20Python%20Django.docx)

API REST con Django y Django REST Framework sobre la base de datos `ventas` (MySQL 8.0). Expone la tabla `cliente`.

## Endpoints

| Método | Ruta           | Descripción              |
|--------|----------------|--------------------------|
| GET    | `/api/cliente` | Lista todos los clientes |
| POST   | `/api/cliente` | Crea un cliente nuevo    |
| —      | `/admin/`      | Panel de administración  |

Ejemplo de cuerpo para crear un cliente (`apellido2`, `ciudad` y `categoria` son opcionales):

```json
{
  "nombre": "Lucía",
  "apellido1": "Martínez",
  "apellido2": "Rojas",
  "ciudad": "Bogotá",
  "categoria": 150
}
```

## Diferencias con la guía

- En el modelo `Cliente`, `apellido2`, `ciudad` y `categoria` admiten `null`, porque en `ventas_db.sql` hay clientes sin esos datos; con los campos obligatorios de la guía, listar esos clientes funciona, pero el modelo no reflejaría la tabla real.
- El modelo usa `managed = False`: la tabla la crea `ventas_db.sql`, no Django.
- `init_command` va dentro de `OPTIONS`, que es donde Django lo lee (la guía lo pone directamente en `default`, donde se ignora).
- La conexión se puede cambiar con variables de entorno (`.env`); sin ellas usa los mismos valores de la guía.

## Estructura

```
api/      App con el modelo Cliente, serializer y vista (Cliente_APIView)
server/   Configuración del proyecto Django
db/       ventas_db.sql: crea y llena la base de datos
bruno/    Peticiones de prueba
```

## Cómo ejecutarlo

### Como en la guía (WampServer y entorno virtual)

1. Inicia WampServer e importa `db/ventas_db.sql` en MySQL (usuario `root`, sin contraseña).
2. Desde esta carpeta, en CMD o PowerShell:

   ```bash
   py -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   py manage.py runserver
   ```

3. Abre <http://127.0.0.1:8000/api/cliente>.

Sin archivo `.env`, el proyecto usa la misma conexión de la guía: base `ventas`, usuario `root`, sin contraseña, `localhost:3306`.

### Con Docker

Desde esta carpeta:

```bash
cp .env.example .env
docker compose up --build
```

La primera vez MySQL ejecuta `db/ventas_db.sql`. Luego abre <http://localhost:8000/api/cliente> o usa la colección de `bruno/` con el entorno `local`.
