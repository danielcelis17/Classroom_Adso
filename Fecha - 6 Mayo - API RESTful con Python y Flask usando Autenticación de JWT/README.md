# Fase 3 — API RESTful con Python y Flask usando Autenticación de JWT

Fuente: `Insumos/2-API Rest Python Flask JWT.docx`. Parte del código de la fase 2
(guía 1 + comercial y pedido con el mismo patrón) y aplica **los pasos de la guía 2 tal
como están escritos**. La base es `Insumos/ventas_db.sql` sin cambios: incluye la tabla
`usuarios` con el usuario `admin` / `admin123`.

La versión mejorada (contraseñas con hash, validaciones, errores en JSON) está en
`00-Version-Oficial-API-Ventas-Flask-JWT/`.

## Ejecutar

```bash
docker compose up -d --build
docker compose logs -f api      # logs (y reinicios del hot reload)
docker compose down -v          # apagar y borrar la BD (se recarga desde database/)
```

- API: http://localhost:5003
- MySQL: `localhost:3313`, usuario `root` sin contraseña (base `ventas`)
- Usuario de prueba de la API: **admin / admin123**
- Bruno: abrir la carpeta `bruno/`, elegir el entorno `local` y ejecutar primero
  `Usuario/Login`; el token queda guardado y lo usan todas las demás peticiones.
  Desde la terminal: `npx @usebruno/cli run -r --env local` dentro de `bruno/`.

## Pasos de la guía

| # | Paso | Implementación |
|---|------|----------------|
| 1–2 | Carpeta `app-ventas` y entorno virtual activo | `app-ventas/` (Docker o `venv` local) |
| 3 | `pip install Flask-JWT-Extended` | `requirements.txt` → `Flask-JWT-Extended==4.7.1` |
| 5 | Proceso de Usuario: crear usuario y login con username y password | `model/usuario.py`, `controller/usuario.py`, `routes/usuario.py` (`user_bp`). La guía no trae el código: se escribió con el mismo patrón de cliente |
| 6 | Probar en Bruno la creación del usuario y el login | `bruno/Usuario/Crear usuario.bru`, `bruno/Usuario/Login.bru` |
| 7 | `from flask_jwt_extended import JWTManager` en `app.py` | `app.py` |
| 8 | `app.config['JWT_SECRET_KEY'] = 'FraseSecretadelaapp'` y `jwt = JWTManager(app)` | `app.py` (igual a la guía) |
| 9 | `create_access_token(identity=user.username)` en el login de `user_bp` | `routes/usuario.py` → `login()` |
| 10 | `@jwt_required()` en las rutas que requieren token | Todas las rutas de `routes/cliente.py`, `routes/comercial.py` y `routes/pedido.py` |
| 11 | Probar en Bruno los endPoints de cliente y comercial | Carpetas `Cliente/`, `Comercial/` y `Pedido/` con `auth: inherit` |

## Endpoints nuevos

| Método | URL | Token | Body | Respuesta |
|--------|-----|-------|------|-----------|
| POST | `/api/usuario` | No | `{"nombre","correo","username","password"}` | `{"message": "OK"}` |
| POST | `/api/login` | No | `{"username","password"}` | `{"access_token": "..."}` · 401 si no coincide |

Cliente, comercial y pedido son los de la fase 2, pero ahora exigen el header
`Authorization: Bearer <access_token>`. Sin token responden **401**
`{"msg": "Missing Authorization Header"}`, el mensaje por defecto de Flask-JWT-Extended.

## Decisiones y advertencias

- **Contraseñas en texto plano.** La tabla `usuarios` de `Insumos/ventas_db.sql` guarda
  `admin123` tal cual (`password VARCHAR(64)`), así que el login compara
  `username` y `password` directamente en el `SELECT`. **Solo sirve para práctica**: si
  alguien lee la tabla ve todas las claves. La versión oficial guarda el hash.
- **Frase secreta corta.** `'FraseSecretadelaapp'` (la de la guía) tiene 19 bytes y PyJWT
  muestra `InsecureKeyLengthWarning` en el log porque HS256 recomienda 32 o más. Funciona
  igual; la versión oficial usa una frase más larga desde el `.env`.
- **El token vence a los 15 minutos** (valor por defecto de Flask-JWT-Extended). Después
  hay que volver a hacer login.
- `username` no es único en la tabla de la guía: se puede registrar dos veces el mismo.

## Pruebas realizadas

- `GET /api/cliente` sin token → 401.
- Login con clave errada → 401; `admin/admin123` → `access_token`.
- Colección de Bruno (Usuario → Cliente → Comercial → Pedido, CRUD completo con token):
  18/18 dos veces seguidas.
