package Paredes.Celis.TiendaDaniel.controller;

import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;
import Paredes.Celis.TiendaDaniel.model.DetalleFactura;
import Paredes.Celis.TiendaDaniel.model.DetalleRequest;
import Paredes.Celis.TiendaDaniel.model.Factura;
import Paredes.Celis.TiendaDaniel.model.Producto;
import Paredes.Celis.TiendaDaniel.repository.DetalleFacturaRepository;
import Paredes.Celis.TiendaDaniel.repository.FacturaRepository;
import Paredes.Celis.TiendaDaniel.repository.ProductoRepository;

import java.util.List;

// CRUD de la tabla detalle_facturas. Cada cambio en una línea ajusta el stock del producto
// y recalcula los totales de su factura.
@RestController
@RequestMapping("api")
public class DetalleFacturaController {

    @Autowired
    private DetalleFacturaRepository dataDetalle;

    @Autowired
    private FacturaRepository dataFactura;

    @Autowired
    private ProductoRepository dataProducto;

    @GetMapping("/detalle-factura")
    public List<DetalleFactura> all() {
        return dataDetalle.findAll();
    }

    @GetMapping("/detalle-factura/{id}")
    public DetalleFactura show(@PathVariable int id) {
        return buscar(id);
    }

    @PostMapping("/detalle-factura")
    @ResponseStatus(HttpStatus.CREATED)
    @Transactional
    public DetalleFactura store(@Valid @RequestBody DetalleRequest datos) {
        if (datos.getFacturaId() == null) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Falta facturaId");
        }
        Factura factura = dataFactura.findById(datos.getFacturaId())
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.BAD_REQUEST, "La factura no existe"));
        Producto producto = buscarProducto(datos.getProductoId());
        FacturaController.descontarStock(producto, datos.getCantidad());

        DetalleFactura detalle = new DetalleFactura();
        detalle.asignarProducto(producto, datos.getCantidad());
        factura.agregarDetalle(detalle);
        factura.recalcularTotales();
        return dataDetalle.save(detalle);
    }

    // Cambia el producto o la cantidad: devuelve el stock de antes y descuenta el nuevo
    @PutMapping("/detalle-factura/{id}")
    @Transactional
    public DetalleFactura update(@PathVariable int id, @Valid @RequestBody DetalleRequest datos) {
        DetalleFactura detalle = buscar(id);
        Producto anterior = detalle.getProducto();
        anterior.setStock(anterior.getStock() + detalle.getCantidad());

        Producto producto = buscarProducto(datos.getProductoId());
        FacturaController.descontarStock(producto, datos.getCantidad());

        detalle.asignarProducto(producto, datos.getCantidad());
        detalle.getFactura().recalcularTotales();
        return dataDetalle.save(detalle);
    }

    // Quita la línea y devuelve el stock. La última línea no se borra: para eso se anula la factura
    @DeleteMapping("/detalle-factura/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    @Transactional
    public void destroy(@PathVariable int id) {
        DetalleFactura detalle = buscar(id);
        Factura factura = detalle.getFactura();
        if (factura.getDetalles().size() == 1) {
            throw new ResponseStatusException(HttpStatus.CONFLICT,
                    "Es la única línea de la factura; para quitarla elimine la factura");
        }
        Producto producto = detalle.getProducto();
        producto.setStock(producto.getStock() + detalle.getCantidad());

        factura.quitarDetalle(detalle);
        factura.recalcularTotales();
    }

    private DetalleFactura buscar(int id) {
        return dataDetalle.findById(id)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Detalle no encontrado"));
    }

    private Producto buscarProducto(int productoId) {
        return dataProducto.findById(productoId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.BAD_REQUEST,
                        "El producto " + productoId + " no existe"));
    }
}
