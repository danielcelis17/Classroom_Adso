<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Autenticación - Sistema Odontología</title>
</head>
<body>
    <h2>Ingreso al Sistema</h2>
    <?php if (isset($_GET['error'])): ?>
        <p style="color: red;">Usuario o clave incorrectos. Intente nuevamente.</p>
    <?php endif; ?>

    <form action="validar_usuario.php" method="POST">
        <label for="usuario">Usuario:</label><br>
        <input type="text" id="usuario" name="usuario" required><br><br>

        <label for="clave">Contraseña:</label><br>
        <input type="password" id="clave" name="clave" required><br><br>

        <input type="submit" value="Ingresar">
    </form>
</body>
</html>