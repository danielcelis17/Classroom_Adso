<?php
require_once 'conexion.php';

$identificacion = $_POST['identificacion'];

$sql = "DELETE FROM usuarios WHERE identificacion='$identificacion'";

if ($conexion->query($sql) === TRUE) {
    echo "Usuario eliminado exitosamente.<br>";
} else {
    echo "Error al eliminar: " . $conexion->error . "<br>";
}
echo "<a href='menu_crud_usuarios.html'>Volver al Menú</a>";
?>