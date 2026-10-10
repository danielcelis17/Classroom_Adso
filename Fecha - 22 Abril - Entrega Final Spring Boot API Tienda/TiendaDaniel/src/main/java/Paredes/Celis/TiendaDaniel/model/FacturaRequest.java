package Paredes.Celis.TiendaDaniel.model;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;

import java.util.List;

// Lo que llega en el body de POST /api/factura (no es una entidad, como LoginUser en la guía 2):
// {"clienteId": 1, "metodoPago": "Nequi/Daviplata", "detalles": [{"productoId": 2, "cantidad": 3}]}
public class FacturaRequest {
    @NotNull
    private Integer clienteId;

    private MetodoPago metodoPago;

    @NotEmpty
    @Valid
    private List<Linea> detalles;

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

    public List<Linea> getDetalles() {
        return detalles;
    }

    public void setDetalles(List<Linea> detalles) {
        this.detalles = detalles;
    }

    public static class Linea {
        @NotNull
        private Integer productoId;

        @NotNull
        @Positive
        private Integer cantidad;

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
}
