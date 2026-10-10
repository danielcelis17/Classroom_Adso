-- =====================================================================
--  Base de datos: ventas
--  Reconstruida a partir de las guías:
--    - API Rest Python Flask / Flask JWT
--    - API Rest Python Django / JWT con DRF
--    - Spring Boot API Rest / Spring Boot Authentication
--
--  Origen de cada tabla:
--    cliente   -> campos tomados del código (model/cliente.py de Flask y
--                 models.py de Django): id, nombre, apellido1, apellido2,
--                 ciudad, categoria
--    comercial -> nombrada en las guías de JWT (ComercialViewSet,
--                 "endPoints de cliente y comercial"); estructura de la
--                 base de ejemplo clásica "ventas"
--    pedido    -> nombrada en la guía JWT de Django (PedidoViewSet);
--                 misma base de ejemplo
--    usuarios  -> CREATE TABLE copiado de la guía de Spring Boot
--                 Authentication (paso 3)
-- =====================================================================

SET NAMES utf8mb4;

DROP DATABASE IF EXISTS ventas;
CREATE DATABASE ventas CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE ventas;

-- ---------------------------------------------------------------------
-- cliente
-- ---------------------------------------------------------------------
CREATE TABLE cliente (
    id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre      VARCHAR(100) NOT NULL,
    apellido1   VARCHAR(100) NOT NULL,
    apellido2   VARCHAR(100),
    ciudad      VARCHAR(100),
    categoria   INT UNSIGNED
);

-- ---------------------------------------------------------------------
-- comercial
-- ---------------------------------------------------------------------
CREATE TABLE comercial (
    id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre      VARCHAR(100) NOT NULL,
    apellido1   VARCHAR(100) NOT NULL,
    apellido2   VARCHAR(100),
    comision    FLOAT
);

-- ---------------------------------------------------------------------
-- pedido
-- ---------------------------------------------------------------------
CREATE TABLE pedido (
    id            INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    total         DOUBLE NOT NULL,
    fecha         DATE,
    id_cliente    INT UNSIGNED NOT NULL,
    id_comercial  INT UNSIGNED NOT NULL,
    FOREIGN KEY (id_cliente)   REFERENCES cliente(id),
    FOREIGN KEY (id_comercial) REFERENCES comercial(id)
);

-- ---------------------------------------------------------------------
-- usuarios (guía Spring Boot Authentication, paso 3)
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS usuarios (
    id        INT(11) NOT NULL AUTO_INCREMENT,
    nombre    VARCHAR(100) NOT NULL,
    correo    VARCHAR(50)  NOT NULL,
    username  VARCHAR(10)  NOT NULL,
    password  VARCHAR(64)  NOT NULL,
    PRIMARY KEY (id)
);

-- =====================================================================
--  Datos de prueba (de la base de ejemplo "ventas")
-- =====================================================================
INSERT INTO cliente VALUES
(1,  'Aarón',     'Rivero',  'Gómez',   'Almería', 100),
(2,  'Adela',     'Salas',   'Díaz',    'Granada', 200),
(3,  'Adolfo',    'Rubio',   'Flores',  'Sevilla', NULL),
(4,  'Adrián',    'Suárez',  NULL,      'Jaén',    300),
(5,  'Marcos',    'Loyola',  'Méndez',  'Almería', 200),
(6,  'María',     'Santana', 'Moreno',  'Cádiz',   100),
(7,  'Pilar',     'Ruiz',    NULL,      'Sevilla', 300),
(8,  'Pepe',      'Ruiz',    'Santana', 'Huelva',  200),
(9,  'Guillermo', 'López',   'Gómez',   'Granada', 225),
(10, 'Daniel',    'Santana', 'Loyola',  'Sevilla', 125);

INSERT INTO comercial VALUES
(1, 'Daniel',  'Sáez',      'Vega',      0.15),
(2, 'Juan',    'Gómez',     'López',     0.13),
(3, 'Diego',   'Flores',    'Salas',     0.11),
(4, 'Marta',   'Herrera',   'Gil',       0.14),
(5, 'Antonio', 'Carretero', 'Ortega',    0.12),
(6, 'Manuel',  'Domínguez', 'Hernández', 0.13),
(7, 'Antonio', 'Vega',      'Hernández', 0.11),
(8, 'Alfredo', 'Ruiz',      'Flores',    0.05);

INSERT INTO pedido VALUES
(1,  150.5,   '2017-10-05', 5, 2),
(2,  270.65,  '2016-09-10', 1, 5),
(3,  65.26,   '2017-10-05', 2, 1),
(4,  110.5,   '2016-08-17', 8, 3),
(5,  948.5,   '2017-09-10', 5, 2),
(6,  2400.6,  '2016-07-27', 7, 1),
(7,  5760,    '2015-09-10', 2, 1),
(8,  1983.43, '2017-10-10', 4, 6),
(9,  2480.4,  '2016-10-10', 8, 3),
(10, 250.45,  '2015-06-27', 8, 2),
(11, 75.29,   '2016-08-17', 3, 7),
(12, 3045.6,  '2017-04-25', 2, 1),
(13, 545.75,  '2019-01-25', 6, 1),
(14, 145.82,  '2017-02-02', 6, 1),
(15, 370.85,  '2019-03-11', 1, 5),
(16, 2389.23, '2019-03-11', 1, 5);

-- Usuario de prueba para el login de Spring Boot.
-- La guía compara la contraseña en texto plano (findByUsernameAndPassword),
-- por eso se guarda así. SOLO para práctica.
INSERT INTO usuarios (nombre, correo, username, password) VALUES
('Administrador', 'admin@ventas.com', 'admin', 'admin123');
