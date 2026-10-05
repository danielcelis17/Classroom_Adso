<?php include_once "../includes/header.php"; ?>

<div class="card">
    <h2>Formulario 2: Salario de Vendedor de Automóviles</h2>
    <form action="ejercicio2_ventas.php" method="POST">
        <div class="form-group">
            <label>Nombre del Vendedor:</label>
            <input type="text" name="vendedor" required>
        </div>
        <div class="form-group">
            <label>Cantidad de Autos Vendidos:</label>
            <input type="number" min="0" name="autos_vendidos" required>
        </div>
        <div class="form-group">
            <label>Valor Total de las Ventas ($):</label>
            <input type="number" min="0" step="1000" name="total_ventas" required>
        </div>
        <button type="submit" class="btn-submit">Calcular Salario Total</button>
    </form>

    <?php
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $vendedor = $_POST['vendedor'];
        $autos = intval($_POST['autos_vendidos']);
        $ventas = floatval($_POST['total_ventas']);

        $salario_basico = 737000;
        $comision_autos = $autos * 50000;
        $comision_porcentaje = $ventas * 0.05;
        $salario_total = $salario_basico + $comision_autos + $comision_porcentaje;

        echo "<div class='result-box'>";
        echo "<h3>Liquidación para: " . htmlspecialchars($vendedor) . "</h3>";
        echo "<p>Salario Básico: $" . number_format($salario_basico, 0, ',', '.') . "</p>";
        echo "<p>Comisión por Autos ($autos × $50.000): $" . number_format($comision_autos, 0, ',', '.') . "</p>";
        echo "<p>Comisión 5% sobre ventas: $" . number_format($comision_porcentaje, 0, ',', '.') . "</p>";
        echo "<h4>Salario Total a Pagar: $" . number_format($salario_total, 0, ',', '.') . "</h4>";
        echo "</div>";
    }
    ?>
</div>

<?php include_once "../includes/footer.php"; ?>