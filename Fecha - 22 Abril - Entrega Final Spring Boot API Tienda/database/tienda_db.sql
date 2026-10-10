DROP DATABASE IF EXISTS tienda;
CREATE DATABASE tienda;
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
