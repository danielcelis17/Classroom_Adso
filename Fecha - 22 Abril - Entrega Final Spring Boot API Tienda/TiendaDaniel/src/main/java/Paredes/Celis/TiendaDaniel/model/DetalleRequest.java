package Paredes.Celis.TiendaDaniel.model;

import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;

// Body de POST y PUT /api/detalle-factura: {"facturaId": 1, "productoId": 2, "cantidad": 3}
// facturaId solo se usa en el POST; una línea no se cambia de factura
public class DetalleRequest {
    private Integer facturaId;

    @NotNull
    private Integer productoId;

    @NotNull
    @Positive
    private Integer cantidad;

    public Integer getFacturaId() {
        return facturaId;
    }

    public void setFacturaId(Integer facturaId) {
        this.facturaId = facturaId;
    }

    public Integer getProductoId() {
        return productoId;
    }

    public void setProductoId(Integer productoId) {
        this.productoId = productoId;
    }

    public Integer getCantidad() {
        return cantidad;
    }

    public void setCantidad(Integer cantidad) {
        this.cantidad = cantidad;
    }
}
