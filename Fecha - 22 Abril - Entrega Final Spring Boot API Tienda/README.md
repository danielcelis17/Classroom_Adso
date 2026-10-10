# Fase 4 — Entrega Final Spring Boot API Tienda

Lleva el patrón de las fases 1 y 3 (model → repository → controller) a la base **`tienda`**
(`INSUMOS/tienda_db.sql`), con el CRUD de sus 4 tablas. Es un proyecto nuevo, **TiendaDaniel**
(Spring Boot 4.0.8, Java 25). No tiene seguridad: el JWT llega en la fase 5.

## Lo que pide la actividad

> Cree un nuevo proyecto en Spring Initializr teniendo en cuenta que en Group van apellido2.apellido1 y en
> Artifact TiendaDeNombre1. Implemente los procesos CRUD de cada uno de las tablas de la base de datos
> tienda_db.sql. Realice las pruebas por medio de Bruno creando una nueva colección y un folder para cada tabla,
> exporte la colección completa y guarde el archivo dentro de la carpeta del proyecto de Spring Boot. Comprima
> la carpeta del proyecto Spring Boot y suba el archivo a la plataforma

| Requisito | Dónde |
|-----------|-------|
| Group `apellido2.apellido1` | `Paredes.Celis` (Daniel Steven Celis Paredes) |
| Artifact `TiendaDeNombre1` | `TiendaDaniel` · package `Paredes.Celis.TiendaDaniel` |
| CRUD de cada tabla | `clientes`, `productos`, `facturas` y `detalle_facturas` (tabla de endpoints abajo) |
| Colección Bruno nueva, un folder por tabla | `TiendaDaniel/bruno/` → `clientes/`, `productos/`, `facturas/`, `detalle_facturas/` |
| Colección exportada dentro del proyecto | `TiendaDaniel/TiendaDaniel.yml` (exportación de Bruno, formato OpenCollection) |
| Proyecto comprimido | **`TiendaDaniel.zip`** (en esta carpeta): este es el archivo que se sube a la plataforma |

## Ejecutar

1. XAMPP con MySQL/MariaDB encendido.
2. Crear la base y cargar los datos de prueba (desde phpMyAdmin → *Importar*, o por consola):

   ```powershell
   C:\xampp\mysql\bin\mysql -u root --default-character-set=utf8mb4 -e "source database/tienda_db.sql"
   C:\xampp\mysql\bin\mysql -u root --default-character-set=utf8mb4 -e "source database/tienda_datos.sql"
   ```

3. Arrancar la API:

   ```powershell
   $env:JAVA_HOME = "C:\Program Files\JetBrains\IntelliJ IDEA 2026.2.2\jbr"
   cd TiendaDaniel
   .\mvnw.cmd spring-boot:run
   ```

API en **http://localhost:8081**. Usa el 8081 para poder correr al mismo tiempo que AppVentas (8080).

## Estructura

```
TiendaDaniel/
├── pom.xml                          groupId Paredes.Celis · artifactId TiendaDaniel
├── TiendaDaniel.yml                 colección de Bruno exportada (OpenCollection YAML)
├── bruno/                           la colección (clientes · productos · facturas · detalle_facturas)
└── src/main/java/Paredes/Celis/TiendaDaniel/
    ├── TiendaDanielApplication.java
    ├── controller/
    │   ├── ClienteController · ProductoController · FacturaController · DetalleFacturaController
    │   └── ManejadorErrores        @RestControllerAdvice: 400 de validación y 409 de datos repetidos
    ├── model/
    │   ├── Cliente · Producto · Factura · DetalleFactura        entidades de las 4 tablas
    │   ├── TipoDocumento (CC, NIT, CE, PP) · MetodoPago (Efectivo, Tarjeta, Transferencia, Nequi/Daviplata)
    │   └── FacturaRequest · FacturaCambios · DetalleRequest     bodies de las peticiones (no son entidades)
    └── repository/   ClienteRepository · ProductoRepository · FacturaRepository · DetalleFacturaRepository
```

## Base de datos (`database/`)

- `tienda_db.sql`: copia del script de `INSUMOS/` (las 4 tablas, sin cambios).
- `tienda_datos.sql`: 5 clientes (uno por cada tipo de documento), 6 productos con IVA de 19 %, 5 % y 0 %,
  y la factura `FAC-000001` con 2 líneas. Se puede volver a ejecutar para dejar la base como al inicio.

Mapeo de columnas: Spring Boot convierte `camelCase` a `snake_case` (`numeroDocumento` → `numero_documento`),
así que las entidades no necesitan `@Column(name = ...)`. El JSON usa los nombres Java (`clienteId`,
`precioUnitario`, `totalPagar`…).

## Endpoints

Todos con prefijo `/api`.

| Tabla | Método | URL | Body | Respuesta |
|-------|--------|-----|------|-----------|
| clientes | GET | `/cliente` · `/cliente/{id}` | — | 200 · 404 |
| | GET | `/cliente/{id}/facturas` | — | 200, facturas del cliente |
| | POST | `/cliente` | **numeroDocumento**, **nombre**, **apellido**, tipoDocumento (`CC` por defecto), telefono, email, direccion, ciudad (`Bogotá` por defecto) | 201 · 400 · 409 documento o email repetido |
| | PUT | `/cliente/{id}` | igual que POST | 200 · 400 · 404 · 409 |
| | DELETE | `/cliente/{id}` | — | 204 · 404 · 409 si tiene facturas |
| productos | GET | `/producto` · `/producto/{id}` | — | 200 · 404 |
| | POST | `/producto` | **nombreProducto**, **precioUnitario** (≥ 0), descripcion, stock (0 por defecto), ivaPorcentaje (0–99.99, 19 por defecto) | 201 · 400 |
| | PUT | `/producto/{id}` | igual que POST | 200 · 400 · 404 |
| | DELETE | `/producto/{id}` | — | 204 · 404 · 409 si está en alguna factura |
| facturas | GET | `/factura` · `/factura/{id}` | — | 200 con cliente y `detalles` · 404 |
| | POST | `/factura` | ver abajo | 201 · 400 |
| | PUT | `/factura/{id}` | **clienteId**, metodoPago | 200 · 400 · 404 |
| | DELETE | `/factura/{id}` | — | 204 (anula: devuelve el stock) · 404 |
| detalle_facturas | GET | `/detalle-factura` · `/detalle-factura/{id}` | — | 200 (con `facturaId`) · 404 |
| | POST | `/detalle-factura` | **facturaId**, **productoId**, **cantidad** (> 0) | 201 · 400 |
| | PUT | `/detalle-factura/{id}` | **productoId**, **cantidad** | 200 · 400 · 404 |
| | DELETE | `/detalle-factura/{id}` | — | 204 · 404 · 409 si es la única línea |

### Crear una factura

```json
{
  "clienteId": 1,
  "metodoPago": "Nequi/Daviplata",
  "detalles": [
    { "productoId": 2, "cantidad": 2 },
    { "productoId": 5, "cantidad": 1 }
  ]
}
```

En una sola transacción (`@Transactional`), la API:

1. Valida que existan el cliente y cada producto, y que haya stock (400 si no).
2. Toma el precio y el IVA **actuales** de cada producto. Por eso se guardan en `precio_venta`:
   si el precio cambia después, la factura conserva el precio con que se vendió.
3. Calcula `subtotal_linea = precio × cantidad`, el IVA de cada línea y los totales de la factura.
4. Descuenta el stock y numera la factura (`FAC-000002`, `FAC-000003`, …).

Si algo falla, no se guarda nada. `metodoPago` es `Efectivo` por defecto. Se acepta el texto de la base
(`"Nequi/Daviplata"`) o el nombre de la constante (`"NEQUI_DAVIPLATA"`).

`PUT /factura/{id}` solo cambia el cliente y el método de pago: el número, la fecha y los totales no se
editan a mano, porque salen de las líneas.

### Detalle de factura

Cada línea pertenece a una factura, así que su CRUD mantiene la factura en orden:

- **POST** agrega una línea a una factura existente, con el precio actual del producto, y descuenta el stock.
- **PUT** cambia el producto o la cantidad: devuelve el stock de antes y descuenta el nuevo.
- **DELETE** quita la línea y devuelve el stock. La última línea no se puede borrar (409): una factura sin
  líneas no tiene sentido, para eso se elimina la factura.
- En los tres casos se recalculan `subtotal`, `total_iva` y `total_pagar` de la factura
  (`Factura.recalcularTotales()`, el mismo cálculo que usa `POST /factura`).

### Errores

```json
// 400 por validación (@Valid)
{"status": 400, "error": "Bad Request", "message": "Datos inválidos",
 "errores": {"nombre": "no debe estar vacío", "email": "debe ser una dirección de correo electrónico con formato correcto"}}
// 400, 404 y 409 de reglas del negocio
{"status": 400, "error": "Bad Request", "message": "Stock insuficiente de Mouse óptico (disponible: 38)", "path": "/api/factura"}
```

## Probar con Bruno

La colección **TiendaDaniel** está en `TiendaDaniel/bruno/`, con un folder por tabla:

| Folder | Peticiones | Qué prueba |
|--------|-----------|------------|
| `clientes` | 10 | listar, obtener, crear, documento repetido (409), datos inválidos (400), actualizar, facturas del cliente, borrar con facturas (409), borrar, obtener borrado (404) |
| `productos` | 8 | listar, obtener, crear, precio negativo (400), actualizar, borrar facturado (409), borrar, obtener borrado (404) |
| `facturas` | 10 | listar, obtener, crear con cálculo de totales, stock descontado, stock insuficiente (400), actualizar (cliente y método de pago), facturas del cliente nuevo, borrar, stock devuelto, obtener borrada (404) |
| `detalle_facturas` | 13 | listar, obtener, agregar línea a `FAC-000001`, totales recalculados, stock insuficiente y cantidad faltante (400), actualizar línea, borrar línea, factura y stock como al inicio, obtener borrado (404) |

Cada folder es independiente: usa los datos de prueba para lo que necesita de las otras tablas y borra lo que
crea, así que se puede ejecutar completo, por folder, o varias veces.

En la app: *Open Collection* → `TiendaDaniel/bruno`, entorno `local`, *Run*. Por consola:

```bash
cd TiendaDaniel/bruno
npx @usebruno/cli run -r --env local
```

Resultado: **41/41 peticiones y 86/86 aserciones OK**, dos veces seguidas, con la base igual al final.
El 409 al borrar la única línea de una factura se probó aparte con curl, porque las facturas de prueba
tienen 2 líneas.

### Exportación y zip

- `TiendaDaniel/TiendaDaniel.yml` es la colección completa exportada: 4 folders, 41 peticiones y el entorno
  `local`. Es el archivo que produce Bruno 4.2.1 con clic derecho sobre la colección → *Share / Export* →
  **Single File (YAML)**: formato [OpenCollection](https://opencollection.com) 1.0.0, nombre `TiendaDaniel.yml`.
  Bruno 4 ya no exporta a `.json`; sus opciones son *Bruno Collection (ZIP)*, *Single File (YAML)*,
  Postman y OpenAPI.
- Se generó con las mismas funciones de Bruno que usa esa opción (`brunoToOpenCollection` de
  `@usebruno/converters`, y `js-yaml` con las mismas opciones). Se comprobó de ida y vuelta: al convertirlo de
  nuevo con `openCollectionToBruno`, las 41 peticiones salen iguales a los `.bru` (método, URL, body, auth,
  aserciones y scripts). Se importa en Bruno con *Import Collection* eligiendo el archivo `.yml`.
- `TiendaDaniel.zip` es la carpeta del proyecto comprimida, sin `target/` ni `.idea/`. Para regenerarlo después
  de un cambio:

  ```powershell
  tar.exe -a -c -f TiendaDaniel.zip TiendaDaniel
  ```

  Se usa `tar.exe`, que viene con Windows, porque `Compress-Archive` de Windows PowerShell 5.1 guarda las rutas
  con `\`, y así el zip no se extrae bien fuera de Windows.

## Agregado respecto a las fases anteriores

| Qué | Para qué |
|-----|----------|
| `spring-boot-starter-validation` + `@Valid`, `@NotBlank`, `@Email`, `@PositiveOrZero`… | Responder 400 con el detalle por campo, en vez de un error de la base |
| `@PrePersist` en `Cliente` y `Producto` | Aplicar los mismos `DEFAULT` de la tabla (CC, Bogotá, stock 0, IVA 19) y devolverlos en la respuesta |
| `BigDecimal` para dinero | `DECIMAL(12,2)` exacto, sin errores de redondeo de `double` |
| `AttributeConverter` en `MetodoPago` | `Nequi/Daviplata` no es un nombre válido para una constante Java |
| `@JsonProperty(access = READ_ONLY)` en ids y `fechaRegistro` | Que el cliente no pueda enviarlos en el body |
| `@Transactional` en factura y detalle | Stock y totales cambian juntos, o no cambia nada |
