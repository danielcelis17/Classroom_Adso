package Paredes.Celis.TiendaDaniel.model;

import jakarta.validation.constraints.NotNull;

// Body de PUT /api/factura/{id}: solo se cambian el cliente y el método de pago.
// Número, fecha y totales no se editan; las líneas se cambian en /api/detalle-factura
public class FacturaCambios {
    @NotNull
    private Integer clienteId;

    private MetodoPago metodoPago;

    public Integer getClienteId() {
        return clienteId;
    }

    public void setClienteId(Integer clienteId) {
        this.clienteId = clienteId;
    }

    public MetodoPago getMetodoPago() {
        return metodoPago;
    }

    public void setMetodoPago(MetodoPago metodoPago) {
        this.metodoPago = metodoPago;
    }
}
