-- =====================================================================
--  Datos de prueba para la base tienda
--  Requiere haber ejecutado antes INSUMOS/tienda_db.sql (crea las tablas).
--  Se puede volver a ejecutar: borra los datos y reinicia los contadores.
-- =====================================================================
USE tienda;
SET NAMES utf8mb4;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE detalle_facturas;
TRUNCATE TABLE facturas;
TRUNCATE TABLE productos;
TRUNCATE TABLE clientes;
SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO clientes (tipo_documento, numero_documento, nombre, apellido, telefono, email, direccion, ciudad) VALUES
('CC',  '1012345678', 'Laura',   'Martínez', '3001234567', 'laura.martinez@correo.com', 'Calle 45 # 12-30',     'Bogotá'),
('CC',  '1023456789', 'Andrés',  'Gómez',    '3112345678', 'andres.gomez@correo.com',   'Carrera 7 # 80-15',    'Bogotá'),
('CE',  'E-9876543',  'Sofía',   'Ramírez',  '3203456789', 'sofia.ramirez@correo.com',  'Avenida 68 # 23-10',   'Medellín'),
('NIT', '900123456-7','Comercializadora', 'Andina SAS', '6017654321', 'compras@andina.com.co', 'Calle 100 # 19-61', 'Bogotá'),
('PP',  'AB1234567',  'Michael', 'Brown',    '3154567890', 'michael.brown@correo.com',  'Carrera 43A # 1-50',   'Cali');

INSERT INTO productos (nombre_producto, descripcion, precio_unitario, stock, iva_porcentaje) VALUES
('Teclado inalámbrico',   'Teclado en español con receptor USB',       85000.00, 25, 19.00),
('Mouse óptico',          'Mouse USB de 1600 DPI',                      35000.00, 38, 19.00),
('Monitor 24 pulgadas',   'Monitor Full HD IPS',                       650000.00, 10, 19.00),
('Cable HDMI 2 m',        'Cable HDMI 2.0',                             18000.00, 60, 19.00),
('Libro Spring Boot',     'Guía práctica de Spring Boot',              120000.00, 14,  0.00),
('Café de Colombia 500 g','Café molido tostión media',                  28000.00, 30,  5.00);

-- Factura de ejemplo: 2 mouse (70.000 + IVA 13.300) y 1 libro (120.000, sin IVA).
-- El stock de esos productos ya está descontado arriba (40 → 38 y 15 → 14).
INSERT INTO facturas (numero_factura, fecha_emision, cliente_id, subtotal, total_iva, total_pagar, metodo_pago) VALUES
('FAC-000001', '2026-10-01 10:30:00', 1, 190000.00, 13300.00, 203300.00, 'Nequi/Daviplata');

INSERT INTO detalle_facturas (factura_id, producto_id, cantidad, precio_venta, subtotal_linea) VALUES
(1, 2, 2,  35000.00,  70000.00),
(1, 5, 1, 120000.00, 120000.00);
