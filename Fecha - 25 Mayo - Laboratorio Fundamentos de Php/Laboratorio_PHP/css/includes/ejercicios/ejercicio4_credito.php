<?php include_once "../includes/header.php"; ?>

<div class="card">
    <h2>Formulario 4: Tabla de Amortización de Crédito</h2>
    <form action="ejercicio4_credito.php" method="POST">
        <div class="form-group">
            <label>Cédula del Cliente:</label>
            <input type="text" name="cedula" required>
        </div>
        <div class="form-group">
            <label>Nombre del Cliente:</label>
            <input type="text" name="cliente" required>
        </div>
        <div class="form-group">
            <label>Monto del Crédito ($):</label>
            <input type="number" min="1000" name="monto" required>
        </div>
        <div class="form-group">
            <label>Tasa de Interés Mensual (%):</label>
            <input type="number" step="0.01" min="0.1" name="tasa" required>
        </div>
        <div class="form-group">
            <label>Plazo en Meses:</label>
            <input type="number" min="1" max="360" name="plazo" required>
        </div>
        <button type="submit" class="btn-submit">Generar Tabla de Amortización</button>
    </form>

    <?php
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $cedula = $_POST['cedula'];
        $cliente = $_POST['cliente'];
        $monto = floatval($_POST['monto']);
        $i = floatval($_POST['tasa']) / 100;
        $n = intval($_POST['plazo']);

        $factor = pow(1 + $i, $n);
        $cuota_fija = $monto * ($i * $factor) / ($factor - 1);

        echo "<div class='result-box'>";
        echo "<h3>Tabla de Amortización</h3>";
        echo "<p><strong>Cédula:</strong> " . htmlspecialchars($cedula) . " | <strong>Cliente:</strong> " . htmlspecialchars($cliente) . "</p>";
        echo "<p><strong>Monto:</strong> $" . number_format($monto, 2, ',', '.') . " | <strong>Tasa:</strong> " . ($_POST['tasa']) . "% | <strong>Plazo:</strong> $n meses</p>";
        echo "<h4>Cuota Fija Mensual: $" . number_format($cuota_fija, 2, ',', '.') . "</h4>";
        echo "</div>";

        echo "<table>";
        echo "<thead><tr><th># Cuota</th><th>Saldo Inicial</th><th>Cuota Fija</th><th>Interés</th><th>Abono a Capital</th><th>Saldo Final</th></tr></thead><tbody>";

        $saldo_inicial = $monto;
        for ($mes = 1; $mes <= $n; $mes++) {
            $interes = $saldo_inicial * $i;
            $abono_capital = $cuota_fija - $interes;
            $saldo_final = $saldo_inicial - $abono_capital;
            if ($mes == $n || abs($saldo_final) < 0.01) $saldo_final = 0.00;

            echo "<tr>";
            echo "<td style='text-align:center;'>$mes</td>";
            echo "<td>$" . number_format($saldo_inicial, 2, ',', '.') . "</td>";
            echo "<td>$" . number_format($cuota_fija, 2, ',', '.') . "</td>";
            echo "<td>$" . number_format($interes, 2, ',', '.') . "</td>";
            echo "<td>$" . number_format($abono_capital, 2, ',', '.') . "</td>";
            echo "<td>$" . number_format($saldo_final, 2, ',', '.') . "</td>";
            echo "</tr>";

            $saldo_inicial = $saldo_final;
        }
        echo "</tbody></table>";
    }
    ?>
</div>

<?php include_once "../includes/footer.php"; ?>