package Paredes.Celis.TiendaDaniel.model;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.persistence.*;

import java.math.BigDecimal;

@Entity
@Table(name = "detalle_facturas")
public class DetalleFactura {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int detalleId;

    // La factura ya contiene sus detalles; no se repite dentro de cada línea
    @ManyToOne
    @JoinColumn(name = "factura_id", nullable = false)
    @JsonIgnore
    private Factura factura;

    @ManyToOne
    @JoinColumn(name = "producto_id", nullable = false)
    private Producto producto;

    private Integer cantidad;
    private BigDecimal precioVenta;
    private BigDecimal subtotalLinea;

    public DetalleFactura() {
    }

    public int getDetalleId() {
        return detalleId;
    }

    public Factura getFactura() {
        return factura;
    }

    // Solo el id de la factura en el JSON, para saber a cuál pertenece la línea en /api/detalle-factura
    @JsonProperty("facturaId")
    public Integer getFacturaId() {
        return factura != null ? factura.getFacturaId() : null;
    }

    // Toma el precio actual del producto y calcula el subtotal de la línea
    public void asignarProducto(Producto producto, int cantidad) {
        this.producto = producto;
        this.cantidad = cantidad;
        this.precioVenta = producto.getPrecioUnitario();
        this.subtotalLinea = producto.getPrecioUnitario().multiply(BigDecimal.valueOf(cantidad));
    }

    public void setFactura(Factura factura) {
        this.factura = factura;
    }

    public Producto getProducto() {
        return producto;
    }

    public void setProducto(Producto producto) {
        this.producto = producto;
    }

    public Integer getCantidad() {
        return cantidad;
    }

    public void setCantidad(Integer cantidad) {
        this.cantidad = cantidad;
    }

    public BigDecimal getPrecioVenta() {
        return precioVenta;
    }

    public void setPrecioVenta(BigDecimal precioVenta) {
        this.precioVenta = precioVenta;
    }

    public BigDecimal getSubtotalLinea() {
        return subtotalLinea;
    }

    public void setSubtotalLinea(BigDecimal subtotalLinea) {
        this.subtotalLinea = subtotalLinea;
    }

    @Override
    public String toString() {
        return "DetalleFactura{" +
                "detalleId=" + detalleId +
                ", producto=" + (producto != null ? producto.getProductoId() : null) +
                ", cantidad=" + cantidad +
                ", subtotalLinea=" + subtotalLinea +
                '}';
    }
}
