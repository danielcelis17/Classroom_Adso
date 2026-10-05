<?php
require_once 'conexion.php';

$identificacion = $_POST['identificacion'];
$nombre = $_POST['nombre'];
$usuario = $_POST['usuario'];
$clave = $_POST['clave'];

$sql = "INSERT INTO usuarios (identificacion, nombre, usuario, clave) VALUES ('$identificacion', '$nombre', '$usuario', '$clave')";

if ($conexion->query($sql) === TRUE) {
    echo "Usuario creado exitosamente.<br>";
} else {
    echo "Error al crear usuario: " . $conexion->error . "<br>";
}
echo "<a href='menu_crud_usuarios.html'>Volver al Menú</a>";
?>