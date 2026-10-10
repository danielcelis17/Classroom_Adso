package Paredes.Celis.TiendaDaniel.model;

import jakarta.persistence.*;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "facturas")
public class Factura {
    private static final BigDecimal CIEN = new BigDecimal("100");

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int facturaId;
    private String numeroFactura;
    private LocalDateTime fechaEmision;

    @ManyToOne
    @JoinColumn(name = "cliente_id", nullable = false)
    private Cliente cliente;

    private BigDecimal subtotal;
    private BigDecimal totalIva;
    private BigDecimal totalPagar;
    private MetodoPago metodoPago;

    @OneToMany(mappedBy = "factura", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<DetalleFactura> detalles = new ArrayList<>();

    public Factura() {
    }

    public void agregarDetalle(DetalleFactura detalle) {
        detalle.setFactura(this);
        detalles.add(detalle);
    }

    public void quitarDetalle(DetalleFactura detalle) {
        detalles.remove(detalle);
        detalle.setFactura(null);
    }

    // Subtotal, IVA y total salen de las líneas: se llama al crear la factura
    // y cada vez que se agrega, cambia o quita un detalle
    public void recalcularTotales() {
        BigDecimal suma = BigDecimal.ZERO;
        BigDecimal iva = BigDecimal.ZERO;
        for (DetalleFactura detalle : detalles) {
            suma = suma.add(detalle.getSubtotalLinea());
            iva = iva.add(detalle.getSubtotalLinea()
                    .multiply(detalle.getProducto().getIvaPorcentaje())
                    .divide(CIEN, 2, RoundingMode.HALF_UP));
        }
        subtotal = suma;
        totalIva = iva;
        totalPagar = suma.add(iva);
    }

    public int getFacturaId() {
        return facturaId;
    }

    public String getNumeroFactura() {
        return numeroFactura;
    }

    public void setNumeroFactura(String numeroFactura) {
        this.numeroFactura = numeroFactura;
    }

    public LocalDateTime getFechaEmision() {
        return fechaEmision;
    }

    public void setFechaEmision(LocalDateTime fechaEmision) {
        this.fechaEmision = fechaEmision;
    }

    public Cliente getCliente() {
        return cliente;
    }

    public void setCliente(Cliente cliente) {
        this.cliente = cliente;
    }

    public BigDecimal getSubtotal() {
        return subtotal;
    }

    public void setSubtotal(BigDecimal subtotal) {
        this.subtotal = subtotal;
    }

    public BigDecimal getTotalIva() {
        return totalIva;
    }

    public void setTotalIva(BigDecimal totalIva) {
        this.totalIva = totalIva;
    }

    public BigDecimal getTotalPagar() {
        return totalPagar;
    }

    public void setTotalPagar(BigDecimal totalPagar) {
        this.totalPagar = totalPagar;
    }

    public MetodoPago getMetodoPago() {
        return metodoPago;
    }

    public void setMetodoPago(MetodoPago metodoPago) {
        this.metodoPago = metodoPago;
    }

    public List<DetalleFactura> getDetalles() {
        return detalles;
    }

    @Override
    public String toString() {
        return "Factura{" +
                "facturaId=" + facturaId +
                ", numeroFactura='" + numeroFactura + '\'' +
                ", totalPagar=" + totalPagar +
                ", metodoPago=" + metodoPago +
                '}';
    }
}
