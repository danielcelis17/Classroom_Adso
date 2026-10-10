-- =====================================================================
--  Base de datos: tienda
--  Tablas clientes, productos, facturas y detalle_facturas: copiadas de
--  Insumos/tienda_db.sql (sin cambios en su estructura).
--  Agregado para la fase 4:
--    - SET NAMES / CHARACTER SET utf8mb4 para que las tildes y ñ se guarden bien
--    - tabla usuarios (login con JWT, igual que en la fase 3)
--    - datos de prueba
-- =====================================================================

SET NAMES utf8mb4;

DROP DATABASE IF EXISTS tienda;
CREATE DATABASE tienda CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE tienda;


CREATE TABLE clientes (
    cliente_id INT AUTO_INCREMENT PRIMARY KEY,
    tipo_documento ENUM('CC', 'NIT', 'CE', 'PP') DEFAULT 'CC',
    numero_documento VARCHAR(15) NOT NULL UNIQUE,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    telefono VARCHAR(15),
    email VARCHAR(100) UNIQUE,
    direccion VARCHAR(150),
    ciudad VARCHAR(50) DEFAULT 'Bogotá',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ;


CREATE TABLE productos (
    producto_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_producto VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio_unitario DECIMAL(12, 2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    iva_porcentaje DECIMAL(4, 2) DEFAULT 19.00
) ;


CREATE TABLE facturas (
    factura_id INT AUTO_INCREMENT PRIMARY KEY,
    numero_factura VARCHAR(20) NOT NULL UNIQUE,
    fecha_emision DATETIME DEFAULT CURRENT_TIMESTAMP,
    cliente_id INT NOT NULL,
    subtotal DECIMAL(12, 2) NOT NULL,
    total_iva DECIMAL(12, 2) NOT NULL,
    total_pagar DECIMAL(12, 2) NOT NULL,
    metodo_pago ENUM('Efectivo', 'Tarjeta', 'Transferencia', 'Nequi/Daviplata') DEFAULT 'Efectivo',
    CONSTRAINT fk_factura_cliente FOREIGN KEY (cliente_id)
        REFERENCES clientes(cliente_id) ON DELETE RESTRICT ON UPDATE CASCADE
) ;


CREATE TABLE detalle_facturas (
    detalle_id INT AUTO_INCREMENT PRIMARY KEY,
    factura_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL,
    precio_venta DECIMAL(12, 2) NOT NULL,
    subtotal_linea DECIMAL(12, 2) NOT NULL,
    CONSTRAINT fk_detalle_factura FOREIGN KEY (factura_id)
        REFERENCES facturas(factura_id) ON DELETE CASCADE,
    CONSTRAINT fk_detalle_producto FOREIGN KEY (producto_id)
        REFERENCES productos(producto_id) ON DELETE RESTRICT
) ;


-- ---------------------------------------------------------------------
-- usuarios (login JWT). password = hash de werkzeug, username único.
-- ---------------------------------------------------------------------
CREATE TABLE usuarios (
    id        INT NOT NULL AUTO_INCREMENT,
    nombre    VARCHAR(100) NOT NULL,
    correo    VARCHAR(50)  NOT NULL,
    username  VARCHAR(50)  NOT NULL UNIQUE,
    password  VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);


-- =====================================================================
--  Datos de prueba
-- =====================================================================

-- Usuario de la API: admin / admin123
-- (hash generado con werkzeug.security.generate_password_hash('admin123'))
INSERT INTO usuarios (nombre, correo, username, password) VALUES
('Administrador', 'admin@tienda.com', 'admin', 'scrypt:32768:8:1$qgvyvcKKS962xhI4$4b6ebf4a351661febd6ad5b56848d12f0842ca7ea36992dc39e958dfebebbd4779bdc455614eb435b4f20c928e8b593e75f82058b215eb7b346993d064cb5801');

INSERT INTO clientes (tipo_documento, numero_documento, nombre, apellido, telefono, email, direccion, ciudad) VALUES
('CC',  '1012345678', 'Laura',    'Gómez',     '3101234567', 'laura.gomez@correo.com',  'Calle 45 # 12-30',     'Bogotá'),
('CC',  '80765432',   'Andrés',   'Martínez',  '3157654321', 'andres.mtz@correo.com',   'Carrera 7 # 80-15',    'Bogotá'),
('CE',  'E4567890',   'Valentina','Rossi',     '3209876543', 'vrossi@correo.com',       'Av. 6N # 23-45',       'Cali'),
('NIT', '900123456-7','Distribuidora', 'El Ahorro', '6017451234', 'compras@elahorro.com', 'Calle 13 # 68-20', 'Bogotá'),
('CC',  '1098765432', 'Camilo',   'Peña',      '3004567890', NULL,                      'Carrera 50 # 10-11',   'Medellín');

INSERT INTO productos (nombre_producto, descripcion, precio_unitario, stock, iva_porcentaje) VALUES
('Arroz Diana 500 g',        'Arroz blanco de grano largo',           2800.00, 98,  5.00),
('Aceite Premier 1 L',       'Aceite vegetal de soya',               12500.00, 49, 19.00),
('Café Sello Rojo 250 g',    'Café tostado y molido',                 9800.00, 80,  5.00),
('Leche Alquería 1 L',       'Leche entera UHT',                      4200.00, 120, 0.00),
('Detergente Ariel 1 kg',    'Detergente en polvo',                  15900.00, 40, 19.00),
('Gaseosa Postobón 1.5 L',   'Bebida gaseosa sabor manzana',          5200.00, 60, 19.00);

-- Factura de ejemplo: 2 x Arroz (IVA 5 %) + 1 x Aceite (IVA 19 %)
--   subtotal  = 2*2800 + 12500        = 18100.00
--   total_iva = 5600*0.05 + 12500*0.19 = 280 + 2375 = 2655.00
--   total     = 20755.00
INSERT INTO facturas (numero_factura, cliente_id, subtotal, total_iva, total_pagar, metodo_pago) VALUES
('FAC-000001', 1, 18100.00, 2655.00, 20755.00, 'Nequi/Daviplata');

INSERT INTO detalle_facturas (factura_id, producto_id, cantidad, precio_venta, subtotal_linea) VALUES
(1, 1, 2,  2800.00,  5600.00),
(1, 2, 1, 12500.00, 12500.00);
