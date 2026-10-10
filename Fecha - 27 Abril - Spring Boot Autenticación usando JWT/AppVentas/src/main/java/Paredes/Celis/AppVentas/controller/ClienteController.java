package Paredes.Celis.AppVentas.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;
import Paredes.Celis.AppVentas.model.Cliente;
import Paredes.Celis.AppVentas.repository.ClienteRepository;

import java.util.List;

@RestController
@RequestMapping("api")
public class ClienteController {

    @Autowired
    private ClienteRepository dataCliente;

    @GetMapping("/cliente")
    public List<Cliente> all() {
        return dataCliente.findAll();
    }

    @GetMapping("/cliente/{id}")
    public Cliente show(@PathVariable int id) {
        return buscar(id);
    }

    @PostMapping("/cliente")
    public Cliente store(@RequestBody Cliente cliente) {
        return dataCliente.save(cliente);
    }

    @PutMapping("/cliente/{id}")
    public Cliente update(@PathVariable int id, @RequestBody Cliente datos) {
        Cliente cliente = buscar(id);
        cliente.setNombre(datos.getNombre());
        cliente.setApellido1(datos.getApellido1());
        cliente.setApellido2(datos.getApellido2());
        cliente.setCiudad(datos.getCiudad());
        cliente.setCategoria(datos.getCategoria());
        return dataCliente.save(cliente);
    }

    @DeleteMapping("/cliente/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void destroy(@PathVariable int id) {
        buscar(id);
        try {
            dataCliente.deleteById(id);
        } catch (DataIntegrityViolationException e) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "El cliente tiene pedidos");
        }
    }

    private Cliente buscar(int id) {
        return dataCliente.findById(id)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Cliente no encontrado"));
    }
}
