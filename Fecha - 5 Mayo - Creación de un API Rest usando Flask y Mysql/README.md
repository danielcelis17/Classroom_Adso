# Fase 1 — Creación de un API Rest usando Flask y MySQL

Fuente: `Insumos/1-API Rest Python Flask.docx` + `Insumos/ventas_db.sql`.

El código de `app-ventas/` es **el de la guía, paso a paso**, con una sola corrección
(marcada con un comentario en el código). La versión mejorada está en
`00-Version-Oficial-API-Ventas-Flask-JWT/`.

## Ejecutar

```bash
docker compose up -d --build
docker compose logs -f api      # logs (y reinicios del hot reload)
docker compose down -v          # apagar y borrar la BD (se recarga desde database/)
```

- API: http://localhost:5001
- MySQL: `localhost:3311`, usuario `root` **sin contraseña** (base `ventas`)
- Bruno: abrir la carpeta `bruno/` y elegir el entorno `local`
  (o `npx @usebruno/cli run -r --env local` dentro de `bruno/`)

### Sin Docker (como dice la guía, con XAMPP)

Importar `database/ventas_db.sql` en el MySQL de XAMPP y:

```bash
cd app-ventas
py -m venv venv
venv\Scripts\activate
pip install flask pymysql
python app.py                   # http://localhost:5000
```

## Pasos de la guía

| # | Paso | Archivo |
|---|------|---------|
| 1 | Carpeta del proyecto | `app-ventas/` |
| 2–4 | Entorno virtual + `pip install flask pymysql` | `requirements.txt` (+ `cryptography`, que PyMySQL necesita con MySQL 8) |
| 6 | `app.py` con la ruta `/` | `app.py` |
| 7 | Probar `http://localhost:5000` en Bruno | `bruno/01 Home.bru` |
| 8 | `config/db.py` con `conexion()` | `config/db.py` (igual a la guía) |
| 9 | `model/cliente.py` | `model/cliente.py` (igual a la guía) |
| 10 | `controller/cliente.py` | `controller/cliente.py` (igual, salvo la corrección 1) |
| 11 | `routes/cliente.py` con `cliente_bp` | `routes/cliente.py` (igual a la guía) |
| 12 | Registrar el Blueprint con prefijo `/api` | `app.py` (igual a la guía) |

## Cómo corre el código de la guía en Docker sin modificarlo

- `config/db.py` usa `host='localhost'`, `user='root'`, `password=''`. En el
  `docker-compose.yml` la API comparte la red del contenedor de MySQL
  (`network_mode: service:db`), así que `localhost` es MySQL; y MySQL se crea con
  `root` sin contraseña (`MYSQL_ALLOW_EMPTY_PASSWORD`), como el de XAMPP.
- `app.py` corre con `host="localhost"`, que no se puede alcanzar desde fuera del
  contenedor. El `Dockerfile` arranca la app con `flask run --host 0.0.0.0 --debug`, que
  no ejecuta el bloque `if __name__ == '__main__'`. `--debug` activa el **hot reload**.

## Correcciones respecto a la guía

1. **`get_cliente` devolvía los datos corridos.** Con `SELECT *` la fila llega como
   `(id, nombre, apellido1, …)`, pero el constructor es
   `Cliente(nombre, apellido1, id, …)`, y `Cliente(*registro)` dejaba el id en `nombre`.
   Se piden las columnas en el orden del constructor:
   `SELECT nombre, apellido1, id, apellido2, ciudad, categoria ...`.

## Comportamientos de la guía que se dejaron igual

Funcionan, pero están corregidos en la versión oficial:

- `GET /api/cliente` devuelve cada cliente como un arreglo `[id, nombre, ...]` sin nombres de
  campo, porque `get_clientes` devuelve `registros` y no `user_objects`.
- `GET /api/cliente/<id>` de un id que no existe responde **500**: `fetchone()` devuelve
  `None` y `Cliente(*None)` falla.
- `PUT` y `DELETE` de un id que no existe responden `{"message": "OK"}`.
- Las tildes salen escapadas (`"Aarón"`): es JSON válido y Bruno las muestra bien.
- `POST` responde 200 (no 201) y no devuelve el id creado. Por eso en Bruno
  `03 Listar clientes` guarda el id del último cliente y `Obtener`/`Actualizar`/`Eliminar` lo usan.

## Endpoints

| Método | URL | Body | Respuesta |
|--------|-----|------|-----------|
| GET | `/` | — | `{"message": "Bienvenido a la API de Tareas con MySQL"}` |
| GET | `/api/cliente` | — | `{"clientes": [[id, nombre, apellido1, apellido2, ciudad, categoria], ...]}` |
| GET | `/api/cliente/<id>` | — | `{"cliente": {...}}` |
| POST | `/api/cliente` | `{"nombre","apellido1","apellido2","ciudad","categoria"}` | `{"message": "OK"}` |
| PUT | `/api/cliente/<id>` | igual que POST | `{"message": "OK"}` |
| DELETE | `/api/cliente/<id>` | — | `{"message": "OK"}` |

## Pruebas realizadas

- La colección de Bruno (Home → Crear → Listar → Obtener → Actualizar → Eliminar) pasa
  6/6 dos veces seguidas.
- `GET /api/cliente/1` → Aarón Rivero Gómez con cada dato en su campo.
- Hot reload: al guardar `app.py` el log muestra `Detected change` y la respuesta cambia sin
  reiniciar el contenedor.
