# Fase 4 — Ajuste Final API Rest Tienda usando Flask, MySQL y JWT

Parte del código de la versión oficial `00-Version-Oficial-API-Ventas-Flask-JWT` (arquitectura en capas + usuarios y JWT según
`Insumos/2-API Rest Python Flask JWT.docx`) y lo lleva a la base **`tienda`**
(`Insumos/tienda_db.sql`): clientes, productos y facturación con detalle.

## Ejecutar

```bash
docker compose up -d --build
docker compose logs -f api      # logs (y reinicios del hot reload)
docker compose down -v          # apagar y borrar la BD (se recarga desde database/)
```

- API: http://localhost:5004
- MySQL: `localhost:3314`, usuario `root`, clave `root` (base `tienda`)
- Usuario de prueba de la API: **admin / admin123**
- Bruno: abrir la carpeta `bruno/`, elegir el entorno `local` y ejecutar primero
  `Usuario/Login`; el token queda guardado y lo usan todas las demás peticiones.
  Desde la terminal: `npx @usebruno/cli run -r --env local` dentro de `bruno/`.

## Estructura

```
app-tienda/
├── app.py                 JWTManager, Blueprints con prefijo /api y manejadores de error
├── config/db.py           conexion() a MySQL (base tienda)
├── model/                 usuario · cliente · producto · factura (Factura + DetalleFactura)
│                          serializar.py → DECIMAL a número y DATETIME a "AAAA-MM-DDTHH:MM:SS"
├── controller/            usuario · cliente · producto · factura (SQL con PyMySQL)
└── routes/                usuario · cliente · producto · factura (Blueprints con @jwt_required())
                           validacion.py → leer_json(), validar_numero(), validar_opcion()
```

## Base de datos (`database/tienda_db.sql`)

Las 4 tablas de `Insumos/tienda_db.sql` sin cambios en su estructura, más:

- `CHARACTER SET utf8mb4` para tildes y ñ (el `DEFAULT 'Bogotá'` incluido).
- Tabla `usuarios` igual a la de la versión oficial (password con hash, username único).
- Datos de prueba: el usuario `admin`, 5 clientes, 6 productos y la factura `FAC-000001`.

## Endpoints

Todos con prefijo `/api`. Salvo `POST /usuario` y `POST /login`, todos exigen
`Authorization: Bearer <token>`.

| Método | URL | Body | Respuesta |
|--------|-----|------|-----------|
| POST | `/usuario` | `{"nombre","correo","username","password"}` | 201 · 409 username repetido |
| POST | `/login` | `{"username","password"}` | `{"access_token"}` · 401 |
| GET | `/usuario/perfil` | — | `{"usuario"}` |
| GET | `/cliente` · `/cliente/<id>` | — | `{"clientes"}` · `{"cliente"}` |
| POST · PUT | `/cliente` · `/cliente/<id>` | **numero_documento**, **nombre**, **apellido**, tipo_documento (`CC`/`NIT`/`CE`/`PP`, por defecto `CC`), telefono, email, direccion, ciudad (por defecto `Bogotá`) | 201 `{"message","cliente_id"}` · 200 |
| DELETE | `/cliente/<id>` | — | 200 · 409 si tiene facturas |
| GET | `/producto` · `/producto/<id>` | — | `{"productos"}` · `{"producto"}` |
| POST · PUT | `/producto` · `/producto/<id>` | **nombre_producto**, **precio_unitario** (≥ 0), descripcion, stock (entero ≥ 0, por defecto 0), iva_porcentaje (0–99.99, por defecto 19) | 201 `{"message","producto_id"}` · 200 |
| DELETE | `/producto/<id>` | — | 200 · 409 si está en alguna factura |
| GET | `/factura` | — | `{"facturas"}` (encabezados) |
| GET | `/factura/<id>` | — | `{"factura"}` con `detalles` |
| POST | `/factura` | `{"cliente_id", "metodo_pago", "detalles": [{"producto_id","cantidad"}]}` | 201 `{"message","factura"}` |
| DELETE | `/factura/<id>` | — | 200 (anula: devuelve el stock) |

`metodo_pago`: `Efectivo` (por defecto), `Tarjeta`, `Transferencia` o `Nequi/Daviplata`.

## Cómo se crea una factura

El cliente de la API solo envía qué productos y cuántos. Todo lo demás lo calcula
`controller/factura.py` en **una sola transacción**:

1. Verifica que exista el cliente (404 si no).
2. Por cada producto lo lee con `SELECT ... FOR UPDATE` (404 si no existe) y verifica el
   stock (409 si no alcanza). El `FOR UPDATE` evita que dos ventas simultáneas vendan
   las mismas unidades.
3. `precio_venta` = precio actual del producto; `subtotal_linea` = precio × cantidad;
   IVA de la línea = `subtotal_linea × iva_porcentaje / 100` (redondeo a centavos).
4. `subtotal` = suma de líneas, `total_iva` = suma de IVA, `total_pagar` = subtotal + IVA.
5. Inserta la factura, la numera `FAC-000123` según su id, inserta los detalles y
   descuenta el stock.
6. Si algo falla hace `rollback`: no queda la factura a medias ni stock descontado.

Si un producto viene repetido en `detalles` se suman las cantidades en una sola línea.
No hay `PUT` de factura: una factura emitida no se edita, se anula (`DELETE`) y se crea
otra. Al anular se devuelve el stock y los detalles se borran en cascada.

## Errores

| Código | Cuándo |
|--------|--------|
| 400 | Body inválido, faltan campos, número negativo o no numérico, valor fuera del ENUM, texto más largo que la columna |
| 401 | Sin token, token inválido o vencido; login incorrecto |
| 404 | Registro o URL inexistente; cliente o producto inexistente al facturar |
| 409 | Documento, email o username repetido; borrar un cliente o producto que está en facturas; stock insuficiente |

## Cambios respecto a la versión oficial

- Base `tienda` en lugar de `ventas`; la app pasa de `app-ventas/` a `app-tienda/`.
- `cliente` se rehace con las columnas de la tabla `clientes`; se quitan `comercial` y
  `pedido`; se agregan `producto` y `factura`.
- `POST` de cliente y producto devuelven el id creado.
- Validación de números y ENUM antes de llegar a MySQL; `DataError` (texto muy largo) → 400.

## Pruebas realizadas

- Sin token → 401. Login `admin/admin123` → token.
- Cliente: crear (toma `CC` y `Bogotá` por defecto), consultar, actualizar, documento
  repetido → 409, `tipo_documento` "XX" → 400, documento de 20 caracteres → 400.
- Producto: crear con y sin `stock`/`iva_porcentaje`, precio negativo → 400.
- Factura con panela ×2 + detergente ×1 + panela ×1 → una línea de panela ×3,
  subtotal 29 400, IVA 3 021 (solo el detergente lleva 19 %), total 32 421, `FAC-000002`,
  stock de la panela 3 → 0.
- Otra factura de panela → 409 stock insuficiente; cliente 999 o producto 999 → 404;
  `detalles` vacío, cantidad 0 o `metodo_pago` "Bitcoin" → 400.
- Borrar el cliente o la panela con factura → 409; anular la factura → stock de la panela
  vuelve a 3; después sí se pueden borrar.
