package Paredes.Celis.TiendaDaniel.controller;

import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;
import Paredes.Celis.TiendaDaniel.model.Producto;
import Paredes.Celis.TiendaDaniel.repository.ProductoRepository;

import java.util.List;

@RestController
@RequestMapping("api")
public class ProductoController {

    @Autowired
    private ProductoRepository dataProducto;

    @GetMapping("/producto")
    public List<Producto> all() {
        return dataProducto.findAll();
    }

    @GetMapping("/producto/{id}")
    public Producto show(@PathVariable int id) {
        return buscar(id);
    }

    @PostMapping("/producto")
    @ResponseStatus(HttpStatus.CREATED)
    public Producto store(@Valid @RequestBody Producto producto) {
        return dataProducto.save(producto);
    }

    @PutMapping("/producto/{id}")
    public Producto update(@PathVariable int id, @Valid @RequestBody Producto datos) {
        Producto producto = buscar(id);
        producto.setNombreProducto(datos.getNombreProducto());
        producto.setDescripcion(datos.getDescripcion());
        producto.setPrecioUnitario(datos.getPrecioUnitario());
        if (datos.getStock() != null) producto.setStock(datos.getStock());
        if (datos.getIvaPorcentaje() != null) producto.setIvaPorcentaje(datos.getIvaPorcentaje());
        return dataProducto.save(producto);
    }

    @DeleteMapping("/producto/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void destroy(@PathVariable int id) {
        buscar(id);
        try {
            dataProducto.deleteById(id);
        } catch (DataIntegrityViolationException e) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "El producto está en alguna factura");
        }
    }

    private Producto buscar(int id) {
        return dataProducto.findById(id)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Producto no encontrado"));
    }
}
