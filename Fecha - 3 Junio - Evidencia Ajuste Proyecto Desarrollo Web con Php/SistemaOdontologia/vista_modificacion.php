<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Modificar Usuario</title>
</head>
<body>
    <h2>Modificar Usuario</h2>
    <form action="controlador_modificar_usuario.php" method="POST">
        <label>Identificación del usuario a modificar:</label><br>
        <input type="text" name="identificacion" required><br><br>

        <label>Nuevo Nombre:</label><br>
        <input type="text" name="nombre" required><br><br>

        <label>Nueva Contraseña:</label><br>
        <input type="password" name="clave" required><br><br>

        <input type="submit" value="Actualizar Usuario">
    </form>
    <p><a href="menu_crud_usuarios.html">Volver al Menú</a></p>
</body>
</html>