# Fase 3 — Implementación Backend usando Spring Boot

Parte del código de la [fase 1](../fase-1-creacion-api-rest/) y completa el backend de la base `ventas`.
Se agregan las entidades `Comercial` y `Pedido`, sus relaciones con `Cliente` y el CRUD completo
(listar, obtener, crear, actualizar y eliminar) de las tres tablas, con el mismo patrón de capas de la guía.

## Ejecutar

Requiere XAMPP con MySQL/MariaDB encendido y la base `ventas` (`INSUMOS/ventas_db.sql`).

```powershell
$env:JAVA_HOME = "C:\Program Files\JetBrains\IntelliJ IDEA 2026.2.2\jbr"
cd AppVentas
.\mvnw.cmd spring-boot:run
```

O en IntelliJ: abrir `AppVentas/` y ejecutar `AppVentasApplication`. API en http://localhost:8080

## Estructura

```
AppVentas/src/main/java/Paredes/Celis/AppVentas/
├── AppVentasApplication.java
├── controller/   ClienteController · ComercialController · PedidoController
├── model/        Cliente (+ pedidos @OneToMany) · Comercial · Pedido (@ManyToOne cliente y comercial)
└── repository/   ClienteRepository · ComercialRepository · PedidoRepository
```

## Relaciones

```
cliente 1 ──< pedido >── 1 comercial
            id_cliente   id_comercial
```

- `Pedido.cliente` y `Pedido.comercial` son `@ManyToOne` con `@JoinColumn(name = "id_cliente" / "id_comercial")`.
- `Cliente.pedidos` es `@OneToMany(mappedBy = "cliente")` y solo se lee. Los pedidos se crean desde `/api/pedido`.
- `@JsonIgnoreProperties("pedidos")` en `Pedido.cliente` corta el ciclo cliente → pedidos → cliente → …
  al generar el JSON. El resultado es el mismo que muestra la captura 13 de la guía de autenticación:
  cada cliente trae sus `pedidos`, y cada pedido trae su `cliente` y su `comercial`.

## Endpoints

Todos con prefijo `/api`. `{recurso}` es `cliente`, `comercial` o `pedido`.

| Método | URL | Respuesta |
|--------|-----|-----------|
| GET | `/{recurso}` | 200, lista |
| GET | `/{recurso}/{id}` | 200 · 404 si no existe |
| POST | `/{recurso}` | 200, el registro creado con su `id` |
| PUT | `/{recurso}/{id}` | 200, el registro actualizado · 404 |
| DELETE | `/{recurso}/{id}` | 204 · 404 · 409 si el cliente o comercial tiene pedidos |

Bodies:

```json
// cliente
{"nombre": "Ana", "apellido1": "Pérez", "apellido2": "Ríos", "ciudad": "Bogotá", "categoria": 150}
// comercial
{"nombre": "Laura", "apellido1": "Gómez", "apellido2": "Díaz", "comision": 0.1}
// pedido: cliente y comercial se envían solo con su id; 400 si alguno no existe
{"total": 350.75, "fecha": "2026-10-10T05:00:00.000Z", "cliente": {"id": 1}, "comercial": {"id": 2}}
```

Los errores responden con el JSON estándar de Spring, con el mensaje incluido
(`spring.web.error.include-message=always`):

```json
{"status": 409, "error": "Conflict", "message": "El cliente tiene pedidos", "path": "/api/cliente/1"}
```

## Probar con Bruno

Abrir `bruno/`, elegir el entorno `local` y ejecutar la colección completa (18 peticiones). La colección
crea un cliente, un comercial y un pedido, los actualiza, prueba los errores 400, 409 y 404, y al final
borra lo que creó. Por eso se puede repetir sin dañar los datos de ejemplo.

```bash
cd bruno
npx @usebruno/cli run -r --env local
```

Resultado: 18/18 peticiones y 29/29 aserciones OK.

## Notas

- `server.error.include-message` (el nombre que aparece en tutoriales) está **retirado** en Spring Boot 4.
  La propiedad nueva es `spring.web.error.include-message`.
- `fecha` es `java.util.Date`, porque así sale en la captura 13 de la guía 2:
  `"fecha": "2016-09-10T05:00:00.000Z"`. La columna es `DATE`; Java la lee como la medianoche en la zona
  horaria del equipo (Bogotá, UTC−5), que en UTC son las 05:00.
- Al crear o actualizar un pedido, `fecha` se envía en ese mismo formato (`"2026-10-10T05:00:00.000Z"`).
  Si se envía solo `"2026-10-10"`, Jackson la toma como medianoche UTC, que en Bogotá todavía es el
  9 de octubre, y en la base queda guardado **un día antes**.
- `categoria` es `int` como en la guía 1 (ver la [fase 1](../fase-1-creacion-api-rest/)).
- El CRUD de `Cliente` conserva los métodos `all()` y `store()` de la guía y agrega `show`, `update` y `destroy`.
