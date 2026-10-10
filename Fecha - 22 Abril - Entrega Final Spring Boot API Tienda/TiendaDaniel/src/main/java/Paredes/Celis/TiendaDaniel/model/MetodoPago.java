package Paredes.Celis.TiendaDaniel.model;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonValue;
import jakarta.persistence.AttributeConverter;
import jakarta.persistence.Converter;

// Valores del ENUM metodo_pago de la tabla facturas. "Nequi/Daviplata" no es un
// nombre válido en Java, así que cada constante guarda el texto exacto de la base.
public enum MetodoPago {
    EFECTIVO("Efectivo"),
    TARJETA("Tarjeta"),
    TRANSFERENCIA("Transferencia"),
    NEQUI_DAVIPLATA("Nequi/Daviplata");

    private final String valor;

    MetodoPago(String valor) {
        this.valor = valor;
    }

    @JsonValue
    public String getValor() {
        return valor;
    }

    @JsonCreator
    public static MetodoPago desdeValor(String valor) {
        for (MetodoPago metodo : values()) {
            if (metodo.valor.equalsIgnoreCase(valor) || metodo.name().equalsIgnoreCase(valor)) {
                return metodo;
            }
        }
        throw new IllegalArgumentException("Método de pago no válido: " + valor);
    }

    // Convierte entre la constante Java y el texto guardado en la columna
    @Converter(autoApply = true)
    public static class ConverterBD implements AttributeConverter<MetodoPago, String> {
        @Override
        public String convertToDatabaseColumn(MetodoPago metodo) {
            return metodo == null ? null : metodo.valor;
        }

        @Override
        public MetodoPago convertToEntityAttribute(String valor) {
            return valor == null ? null : desdeValor(valor);
        }
    }
}
