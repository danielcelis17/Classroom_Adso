# Fase 5 — Spring Boot Autenticación usando JWT (versión final)

Protege la API de la [fase 3](../fase-3-implementacion-backend/) con **Spring Security** y **JWT (JJWT 0.11.5)**,
siguiendo `INSUMOS/2-Spring Boot Authentication_.docx`. `POST /api/login` entrega un token, y todos los demás
endpoints lo exigen en la cabecera `Authorization: Bearer <token>`.

## Ejecutar

Requiere XAMPP con la base `ventas` (`INSUMOS/ventas_db.sql`). Ese script ya crea la tabla `usuarios`
(paso 3 de la guía) con el usuario de prueba **admin / admin123**.

```powershell
$env:JAVA_HOME = "C:\Program Files\JetBrains\IntelliJ IDEA 2026.2.2\jbr"
cd AppVentas
.\mvnw.cmd spring-boot:run
```

API en http://localhost:8080

## Estructura (lo nuevo está marcado con ★)

```
AppVentas/src/main/java/Paredes/Celis/AppVentas/
├── AppVentasApplication.java          ★ clase interna SecurityConfig (paso 12)
├── controller/   Cliente · Comercial · Pedido · ★ UsuarioController (login, addUsuario, getJWTToken)
├── model/        Cliente · Comercial · Pedido · ★ Usuario (@Transient token) · ★ LoginUser
├── repository/   Cliente · Comercial · Pedido · ★ UsuarioRepository (findByUsernameAndPassword)
└── security/     ★ JWTAuthorizationFilter
```

## Pasos de la guía

| Paso | Qué se hizo |
|------|-------------|
| 1–2 | `pom.xml`: `spring-boot-starter-security`, `spring-security-test`, `jjwt-api`, `jjwt-impl` y `jjwt-jackson` 0.11.5 |
| 3 | Tabla `usuarios` (incluida en `INSUMOS/ventas_db.sql`) |
| 4 | `Usuario` con `@Transient private String token` |
| 5 | `LoginUser` (username, password, getters/setters, `toString`) |
| 6 | `UsuarioRepository.findByUsernameAndPassword` |
| 7, 10, 11 | `UsuarioController`: `POST /api/login` (genera el token con `getJWTToken`) y `POST /api/usuario` (`addUsuario`) |
| 8–9 | Package `security` con `JWTAuthorizationFilter` |
| 12 | `SecurityConfig`: agrega el filtro, exige autenticación en todo y deja libre `/api/login` |
| 13 | Pruebas en Bruno (abajo) |

## Cómo funciona

```
POST /api/login {"username","password"}
   └─ UsuarioController busca el usuario → firma un JWT (HS256, 10 min, sub=username,
      authorities=[ROLE_USER]) con JWTAuthorizationFilter.key → lo devuelve en "token"

GET /api/cliente   Authorization: Bearer eyJhbGciOi...
   └─ JWTAuthorizationFilter: ¿hay cabecera "Bearer "? → valida la firma → registra al usuario
      en el SecurityContext → anyRequest().authenticated() lo deja pasar → 200
      Sin token o con un token inválido → 401
```

## Pruebas (paso 13 de la guía)

| Prueba | Resultado |
|--------|-----------|
| a. Todos los Clientes sin token | **401 Unauthorized** |
| b. Login `admin` / `admin123` | **200**, el usuario con `"token": "Bearer eyJhbGciOiJIUzI1NiJ9..."` |
| c. Todos los Clientes con *Auth → Bearer Token* (el token sin la palabra `Bearer`) | **200**, la lista de clientes con sus `pedidos`, igual que la captura 13 de la guía |

El JSON de la prueba c coincide con la captura 13: el cliente 1 Aarón Rivero Gómez (categoría 100) con el
pedido del `"2016-09-10T05:00:00.000Z"` del comercial 5 Antonio Carretero Ortega (comisión 0.12).

En Bruno: abrir `bruno/`, entorno `local`, y ejecutar la colección. *Login* guarda el token (ya sin `Bearer `)
en la variable `{{token}}`, y las demás peticiones lo usan en *Auth → Bearer Token*.

| # | Petición | Esperado |
|---|----------|----------|
| 01–03 | Las 3 pruebas de la guía | 401 · 200 con token · 200 con los datos de la captura 13 |
| 04–06 | Cliente 1, comerciales y pedidos con token | 200 |
| 07 | Crear cliente con token | **401**: limitación del código de la guía (ver abajo). No se guarda nada |
| 08 | `addUsuario` con token | **401**, por la misma razón |

```bash
cd bruno
npx @usebruno/cli run -r --env local
```

Resultado: 8/8 peticiones y 19/19 aserciones OK, dos veces seguidas. La colección no modifica la base.

## Código igual a la guía

`JWTAuthorizationFilter`, `getJWTToken`, `login` y `SecurityConfig` son el código de los pasos 9 a 12 de la
guía, sin agregados. `UsuarioRepository` extiende `JpaRepository<Usuario, Long>` como en la captura del paso 6.
`Usuario` tiene `@Transient token` y `LoginUser` tiene sus getters, setters y `toString` (pasos 4 y 5).

Única diferencia: el método del paso 7 se llama `addUsuario`, como dice el texto de la guía. En la captura
aparece como `store`; el endpoint es el mismo, `POST /api/usuario`.

## Comportamiento del código de la guía (medido, se deja como está)

| Caso | Respuesta | Por qué |
|------|-----------|---------|
| `POST`, `PUT` o `DELETE` con token válido | **401** | Spring Security deja activa la protección CSRF y rechaza la petición (en consola, con log DEBUG: `Invalid CSRF token found`). El rechazo se reenvía a `/error`, que la guía también protege, y termina en 401. La guía solo prueba `GET`, por eso no aparece. Se arreglaría con `.csrf(csrf -> csrf.disable())` |
| Token mal formado o vencido | **401** | El filtro responde 403, pero ese error pasa por `/error` y termina en 401 |
| Token con firma de otra clave (por ejemplo, de antes de reiniciar la app) | **401** y un `ERROR` en consola | `SignatureException` no está en el `catch` de la guía |
| 404 o 409 de los controllers con token | **401** | El mismo reenvío a `/error` protegido. Se arreglaría con `.dispatcherTypeMatchers(DispatcherType.ERROR).permitAll()` |
| Login con credenciales incorrectas | **200** con el cuerpo vacío | `login` devuelve `null` |

## Otras limitaciones (solo para práctica)

- La contraseña se guarda y se compara **en texto plano**, y el login la **devuelve** en el JSON.
  En un proyecto real se guarda con BCrypt (`PasswordEncoder`) y se oculta con `@JsonIgnore`.
- El primer usuario (`admin` / `admin123`) se inserta directo en la base (`INSUMOS/ventas_db.sql`):
  `addUsuario` exige token y además lo bloquea CSRF.
- La clave se genera al azar en cada arranque (`Keys.secretKeyFor`): al reiniciar la app, los tokens
  anteriores dejan de servir.
- En consola aparecen dos avisos esperados: `Using generated security password` (el usuario por defecto de
  `httpBasic`) y `You are asking Spring Security to ignore PathPattern [/api/login]` (Spring recomienda
  `permitAll()` en vez de `web.ignoring()`; se dejó como en la guía).
