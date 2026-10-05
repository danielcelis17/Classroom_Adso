<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Crear Usuario</title>
</head>
<body>
    <h2>Crear Nuevo Usuario</h2>
    <form action="controlador_crear_usuario.php" method="POST">
        <label>Identificación:</label><br>
        <input type="text" name="identificacion" required><br><br>

        <label>Nombre Completo:</label><br>
        <input type="text" name="nombre" required><br><br>

        <label>Usuario:</label><br>
        <input type="text" name="usuario" required><br><br>

        <label>Contraseña:</label><br>
        <input type="password" name="clave" required><br><br>

        <input type="submit" value="Guardar Usuario">
    </form>
    <p><a href="menu_crud_usuarios.html">Volver al Menú</a></p>
</body>
</html>