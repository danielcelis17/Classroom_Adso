<?php
require_once 'conexion.php';

$usuario = $_POST['usuario'];
$clave = $_POST['clave'];

$sql = "SELECT * FROM usuarios WHERE usuario = '$usuario' AND clave = '$clave'";
$resultado = $conexion->query($sql);

if ($resultado && $resultado->num_rows > 0) {
    $datos = $resultado->fetch_assoc();
    echo "<h1>¡Bienvenido/a " . htmlspecialchars($datos['nombre']) . "!</h1>";
    echo "<p><a href='menu_crud_usuarios.html'>Ir al Menú Principal</a></p>";
} else {
    header("Location: ingreso_al_sistema.php?error=1");
    exit();
}
?>