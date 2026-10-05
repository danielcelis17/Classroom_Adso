<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Borrar Usuario</title>
</head>
<body>
    <h2>Borrar Usuario</h2>
    <form action="controlador_borrar_usuario.php" method="POST">
        <label>Identificación del usuario a eliminar:</label><br>
        <input type="text" name="identificacion" required><br><br>

        <input type="submit" value="Eliminar Usuario">
    </form>
    <p><a href="menu_crud_usuarios.html">Volver al Menú</a></p>
</body>
</html>