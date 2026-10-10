package Paredes.Celis.TiendaDaniel.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.persistence.*;
import jakarta.validation.constraints.*;

import java.math.BigDecimal;

@Entity
@Table(name = "productos")
public class Producto {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @JsonProperty(access = JsonProperty.Access.READ_ONLY)
    private int productoId;

    @NotBlank
    @Size(max = 100)
    private String nombreProducto;

    private String descripcion;

    @NotNull
    @PositiveOrZero
    @Digits(integer = 10, fraction = 2)
    private BigDecimal precioUnitario;

    @PositiveOrZero
    private Integer stock;

    @DecimalMin("0.00")
    @DecimalMax("99.99")
    private BigDecimal ivaPorcentaje;

    public Producto() {
    }

    // Los mismos valores por defecto de la tabla (stock 0, IVA 19 %)
    @PrePersist
    void valoresPorDefecto() {
        if (stock == null) stock = 0;
        if (ivaPorcentaje == null) ivaPorcentaje = new BigDecimal("19.00");
    }

    public int getProductoId() {
        return productoId;
    }

    public String getNombreProducto() {
        return nombreProducto;
    }

    public void setNombreProducto(String nombreProducto) {
        this.nombreProducto = nombreProducto;
    }

    public String getDescripcion() {
        return descripcion;
    }

    public void setDescripcion(String descripcion) {
        this.descripcion = descripcion;
    }

    public BigDecimal getPrecioUnitario() {
        return precioUnitario;
    }

    public void setPrecioUnitario(BigDecimal precioUnitario) {
        this.precioUnitario = precioUnitario;
    }

    public Integer getStock() {
        return stock;
    }

    public void setStock(Integer stock) {
        this.stock = stock;
    }

    public BigDecimal getIvaPorcentaje() {
        return ivaPorcentaje;
    }

    public void setIvaPorcentaje(BigDecimal ivaPorcentaje) {
        this.ivaPorcentaje = ivaPorcentaje;
    }

    @Override
    public String toString() {
        return "Producto{" +
                "productoId=" + productoId +
                ", nombreProducto='" + nombreProducto + '\'' +
                ", precioUnitario=" + precioUnitario +
                ", stock=" + stock +
                ", ivaPorcentaje=" + ivaPorcentaje +
                '}';
    }
}
