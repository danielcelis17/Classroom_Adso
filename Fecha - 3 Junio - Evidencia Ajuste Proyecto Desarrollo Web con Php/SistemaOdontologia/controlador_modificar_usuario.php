<?php
require_once 'conexion.php';

$identificacion = $_POST['identificacion'];
$nombre = $_POST['nombre'];
$clave = $_POST['clave'];

$sql = "UPDATE usuarios SET nombre='$nombre', clave='$clave' WHERE identificacion='$identificacion'";

if ($conexion->query($sql) === TRUE) {
    echo "Usuario actualizado exitosamente.<br>";
} else {
    echo "Error al actualizar: " . $conexion->error . "<br>";
}
echo "<a href='menu_crud_usuarios.html'>Volver al Menú</a>";
?>