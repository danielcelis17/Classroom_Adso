<?php include_once "../includes/header.php"; ?>

<div class="card">
    <h2>Formulario 3: Cálculo del Índice de Masa Corporal (IMC)</h2>
    <form action="ejercicio3_imc.php" method="POST">
        <div class="form-group">
            <label>Nombre del Paciente:</label>
            <input type="text" name="paciente" required>
        </div>
        <div class="form-group">
            <label>Peso en Kilogramos (kg):</label>
            <input type="number" step="0.1" min="1" name="peso" required>
        </div>
        <div class="form-group">
            <label>Estatura en Metros (m):</label>
            <input type="number" step="0.01" min="0.5" max="2.5" name="estatura" required>
        </div>
        <button type="submit" class="btn-submit">Calcular IMC</button>
    </form>

    <?php
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $paciente = $_POST['paciente'];
        $peso = floatval($_POST['peso']);
        $estatura = floatval($_POST['estatura']);

        if ($estatura > 0) {
            $imc = $peso / ($estatura * $estatura);

            if ($imc < 18.5) $categoria = "Bajo peso";
            elseif ($imc < 25.0) $categoria = "Peso Normal (Saludable)";
            elseif ($imc < 30.0) $categoria = "Sobrepeso";
            elseif ($imc < 35.0) $categoria = "Obesidad Grado I";
            elseif ($imc < 40.0) $categoria = "Obesidad Grado II";
            else $categoria = "Obesidad Grado III (Mórbida)";

            echo "<div class='result-box'>";
            echo "<h3>Informe Nutricional: " . htmlspecialchars($paciente) . "</h3>";
            echo "<p>IMC Calculado: " . number_format($imc, 2) . "</p>";
            echo "<h4>Categoría: $categoria</h4>";
            echo "</div>";
        }
    }
    ?>
</div>

<?php include_once "../includes/footer.php"; ?>