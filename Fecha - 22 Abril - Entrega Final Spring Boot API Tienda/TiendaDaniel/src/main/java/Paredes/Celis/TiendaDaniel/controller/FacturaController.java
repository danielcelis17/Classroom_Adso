package Paredes.Celis.TiendaDaniel.controller;

import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;
import Paredes.Celis.TiendaDaniel.model.*;
import Paredes.Celis.TiendaDaniel.repository.ClienteRepository;
import Paredes.Celis.TiendaDaniel.repository.FacturaRepository;
import Paredes.Celis.TiendaDaniel.repository.ProductoRepository;

import java.time.LocalDateTime;
import java.util.List;

@RestController
@RequestMapping("api")
public class FacturaController {

    @Autowired
    private FacturaRepository dataFactura;

    @Autowired
    private ClienteRepository dataCliente;

    @Autowired
    private ProductoRepository dataProducto;

    @GetMapping("/factura")
    public List<Factura> all() {
        return dataFactura.findAll();
    }

    @GetMapping("/factura/{id}")
    public Factura show(@PathVariable int id) {
        return buscar(id);
    }

    // Crea la factura con sus líneas: toma el precio y el IVA actuales de cada producto,
    // calcula subtotal, IVA y total, y descuenta el stock. Si algo falla no se guarda nada.
    @PostMapping("/factura")
    @ResponseStatus(HttpStatus.CREATED)
    @Transactional
    public Factura store(@Valid @RequestBody FacturaRequest datos) {
        Factura factura = new Factura();
        factura.setCliente(buscarCliente(datos.getClienteId()));
        factura.setFechaEmision(LocalDateTime.now());
        factura.setMetodoPago(datos.getMetodoPago() != null ? datos.getMetodoPago() : MetodoPago.EFECTIVO);
        factura.setNumeroFactura(siguienteNumero());

        for (FacturaRequest.Linea linea : datos.getDetalles()) {
            Producto producto = dataProducto.findById(linea.getProductoId())
                    .orElseThrow(() -> new ResponseStatusException(HttpStatus.BAD_REQUEST,
                            "El producto " + linea.getProductoId() + " no existe"));
            descontarStock(producto, linea.getCantidad());

            DetalleFactura detalle = new DetalleFactura();
            detalle.asignarProducto(producto, linea.getCantidad());
            factura.agregarDetalle(detalle);
        }

        factura.recalcularTotales();
        return dataFactura.save(factura);
    }

    // Cambia el cliente y el método de pago. Las líneas se editan en /api/detalle-factura
    @PutMapping("/factura/{id}")
    @Transactional
    public Factura update(@PathVariable int id, @Valid @RequestBody FacturaCambios datos) {
        Factura factura = buscar(id);
        factura.setCliente(buscarCliente(datos.getClienteId()));
        if (datos.getMetodoPago() != null) {
            factura.setMetodoPago(datos.getMetodoPago());
        }
        return dataFactura.save(factura);
    }

    // Anula la factura: devuelve el stock de cada producto y borra la factura con su detalle
    @DeleteMapping("/factura/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    @Transactional
    public void destroy(@PathVariable int id) {
        Factura factura = buscar(id);
        for (DetalleFactura detalle : factura.getDetalles()) {
            Producto producto = detalle.getProducto();
            producto.setStock(producto.getStock() + detalle.getCantidad());
        }
        dataFactura.delete(factura);
    }

    // También lo usa DetalleFacturaController
    static void descontarStock(Producto producto, int cantidad) {
        if (producto.getStock() < cantidad) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST,
                    "Stock insuficiente de " + producto.getNombreProducto() + " (disponible: " + producto.getStock() + ")");
        }
        producto.setStock(producto.getStock() - cantidad);
    }

    private Factura buscar(int id) {
        return dataFactura.findById(id)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Factura no encontrada"));
    }

    private Cliente buscarCliente(int clienteId) {
        return dataCliente.findById(clienteId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.BAD_REQUEST, "El cliente no existe"));
    }

    private String siguienteNumero() {
        int ultimo = dataFactura.findTopByOrderByFacturaIdDesc().map(Factura::getFacturaId).orElse(0);
        return String.format("FAC-%06d", ultimo + 1);
    }
}
