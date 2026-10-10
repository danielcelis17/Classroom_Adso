package Paredes.Celis.AppVentas.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;
import Paredes.Celis.AppVentas.model.Cliente;
import Paredes.Celis.AppVentas.model.Comercial;
import Paredes.Celis.AppVentas.model.Pedido;
import Paredes.Celis.AppVentas.repository.ClienteRepository;
import Paredes.Celis.AppVentas.repository.ComercialRepository;
import Paredes.Celis.AppVentas.repository.PedidoRepository;

import java.util.List;

@RestController
@RequestMapping("api")
public class PedidoController {

    @Autowired
    private PedidoRepository dataPedido;

    @Autowired
    private ClienteRepository dataCliente;

    @Autowired
    private ComercialRepository dataComercial;

    @GetMapping("/pedido")
    public List<Pedido> all() {
        return dataPedido.findAll();
    }

    @GetMapping("/pedido/{id}")
    public Pedido show(@PathVariable int id) {
        return buscar(id);
    }

    // Body: {"total": 150.5, "fecha": "2026-10-10", "cliente": {"id": 1}, "comercial": {"id": 2}}
    @PostMapping("/pedido")
    public Pedido store(@RequestBody Pedido pedido) {
        asignarRelaciones(pedido, pedido);
        return dataPedido.save(pedido);
    }

    @PutMapping("/pedido/{id}")
    public Pedido update(@PathVariable int id, @RequestBody Pedido datos) {
        Pedido pedido = buscar(id);
        pedido.setTotal(datos.getTotal());
        pedido.setFecha(datos.getFecha());
        asignarRelaciones(pedido, datos);
        return dataPedido.save(pedido);
    }

    @DeleteMapping("/pedido/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void destroy(@PathVariable int id) {
        buscar(id);
        dataPedido.deleteById(id);
    }

    private Pedido buscar(int id) {
        return dataPedido.findById(id)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Pedido no encontrado"));
    }

    // Reemplaza los {"id": n} del body por el cliente y el comercial reales de la base
    private void asignarRelaciones(Pedido pedido, Pedido datos) {
        if (datos.getTotal() == null || datos.getCliente() == null || datos.getComercial() == null) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "total, cliente y comercial son obligatorios");
        }
        Cliente cliente = dataCliente.findById(datos.getCliente().getId())
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.BAD_REQUEST, "El cliente no existe"));
        Comercial comercial = dataComercial.findById(datos.getComercial().getId())
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.BAD_REQUEST, "El comercial no existe"));
        pedido.setCliente(cliente);
        pedido.setComercial(comercial);
    }
}
