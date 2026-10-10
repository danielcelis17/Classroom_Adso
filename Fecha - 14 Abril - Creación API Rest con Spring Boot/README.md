# Fase 1 — Creación API Rest con Spring Boot

Sigue la guía `INSUMOS/1-Spring Boot API Rest_.docx` paso a paso sobre el proyecto
`INSUMOS/AppVentas.zip` (Spring Boot 4.0.8, Java 25, Maven, package `Paredes.Celis.AppVentas`).

## Ejecutar

Requiere XAMPP con MySQL/MariaDB encendido y la base `ventas` (`INSUMOS/ventas_db.sql`).

- **IntelliJ IDEA:** abrir la carpeta `AppVentas/` → *Trust Project* → ejecutar `AppVentasApplication`.
- **Terminal (PowerShell):**

  ```powershell
  $env:JAVA_HOME = "C:\Program Files\JetBrains\IntelliJ IDEA 2026.2.2\jbr"
  cd AppVentas
  .\mvnw.cmd spring-boot:run
  ```

API en http://localhost:8080

## Estructura

```
AppVentas/src/main/java/Paredes/Celis/AppVentas/
├── AppVentasApplication.java
├── controller/ClienteController.java   GET y POST /api/cliente
├── model/Cliente.java                  entidad de la tabla cliente
└── repository/ClienteRepository.java   JpaRepository<Cliente, Integer> + findByNombre
```

## Endpoints

| Método | URL | Body | Respuesta |
|--------|-----|------|-----------|
| GET | `/api/cliente` | — | 200, lista de clientes |
| POST | `/api/cliente` | `{"nombre","apellido1","apellido2","ciudad","categoria"}` | 200, el cliente guardado con su `id` |

## Probar con Bruno

Abrir la carpeta `bruno/` en Bruno, elegir el entorno `local` y ejecutar
*Todos los Clientes* y *Crear un Cliente*. Desde la terminal (con la app corriendo):

```bash
cd bruno
npx @usebruno/cli run -r --env local
```

## Ajustes respecto a la guía

| Qué | Por qué |
|-----|---------|
| Se agregaron al `pom.xml` Spring Web (`spring-boot-starter-webmvc`), Spring Data JPA, DevTools y MySQL Driver | El `AppVentas.zip` se generó sin las dependencias del paso 1 de la guía (solo traía `spring-boot-starter`) |
| `spring.jpa.show-sql=true` | En la captura se lee `spring.jpa.show=true`, que Spring ignora (queda un comentario en el archivo) |
| Spring Boot 4.0.8 (la guía dice 4.0.5) | Es la versión con la que se generó el `AppVentas.zip` entregado |

El resto es igual a las capturas de la guía: `Cliente` con `int id` e `int categoria`,
`@EntityListeners(AuditingEntityListener.class)`, `ClienteRepository` con `findByNombre(@Param("nombre"))`
y `ClienteController` con `all()` y `store()`.

Como `categoria` es `int` (primitivo), ningún cliente de la base puede tener `categoria` en `NULL`:
Hibernate no puede leer `NULL` en un `int` y `GET /api/cliente` fallaría con 500. Por eso en
`INSUMOS/ventas_db.sql` el cliente 3 (Adolfo Rubio Flores) tiene categoría 100.

Advertencia esperada en consola: `HHH000511: The 5.5.5 version for [MySQLDialect] is no longer supported`.
La MariaDB de XAMPP se reporta como "5.5.5"; no impide que la API funcione.
