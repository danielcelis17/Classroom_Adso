<?php include_once "../includes/header.php"; ?>

<div class="card">
    <h2>Formulario 1: Cálculo de Nota Final</h2>
    <form action="ejercicio1_notas.php" method="POST">
        <div class="form-group">
            <label>Nombre del Estudiante:</label>
            <input type="text" name="estudiante" required>
        </div>
        <div class="form-group">
            <label>Nota Parcial 1 (0.0 - 5.0):</label>
            <input type="number" step="0.1" min="0" max="5" name="parcial1" required>
        </div>
        <div class="form-group">
            <label>Nota Parcial 2 (0.0 - 5.0):</label>
            <input type="number" step="0.1" min="0" max="5" name="parcial2" required>
        </div>
        <div class="form-group">
            <label>Nota Parcial 3 (0.0 - 5.0):</label>
            <input type="number" step="0.1" min="0" max="5" name="parcial3" required>
        </div>
        <div class="form-group">
            <label>Examen Final (0.0 - 5.0):</label>
            <input type="number" step="0.1" min="0" max="5" name="examen_final" required>
        </div>
        <div class="form-group">
            <label>Trabajo Final (0.0 - 5.0):</label>
            <input type="number" step="0.1" min="0" max="5" name="trabajo_final" required>
        </div>
        <button type="submit" class="btn-submit">Calcular Nota Final</button>
    </form>

    <?php
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $estudiante = $_POST['estudiante'];
        $parcial1 = floatval($_POST['parcial1']);
        $parcial2 = floatval($_POST['parcial2']);
        $parcial3 = floatval($_POST['parcial3']);
        $examen_final = floatval($_POST['examen_final']);
        $trabajo_final = floatval($_POST['trabajo_final']);

        $promedio_parciales = ($parcial1 + $parcial2 + $parcial3) / 3;
        $nota_final = ($promedio_parciales * 0.35) + ($examen_final * 0.35) + ($trabajo_final * 0.30);
        $aprobado = $nota_final >= 3.0;

        $clase = $aprobado ? "result-box" : "result-box danger";
        $estado = $aprobado ? "Aprobó" : "No aprobó";

        echo "<div class='$clase'>";
        echo "<h3>Resultados para: " . htmlspecialchars($estudiante) . "</h3>";
        echo "<p>Promedio Parciales (35%): " . number_format($promedio_parciales, 2) . "</p>";
        echo "<p>Examen Final (35%): " . number_format($examen_final, 2) . "</p>";
        echo "<p>Trabajo Final (30%): " . number_format($trabajo_final, 2) . "</p>";
        echo "<p><strong>Nota Definitiva: " . number_format($nota_final, 2) . "</strong></p>";
        echo "<h4>Estado: $estado</h4>";
        echo "</div>";
    }
    ?>
</div>

<?php include_once "../includes/footer.php"; ?>