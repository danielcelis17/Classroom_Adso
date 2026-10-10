package Paredes.Celis.TiendaDaniel.controller;

import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;
import Paredes.Celis.TiendaDaniel.model.Cliente;
import Paredes.Celis.TiendaDaniel.model.Factura;
import Paredes.Celis.TiendaDaniel.repository.ClienteRepository;
import Paredes.Celis.TiendaDaniel.repository.FacturaRepository;

import java.util.List;

@RestController
@RequestMapping("api")
public class ClienteController {

    @Autowired
    private ClienteRepository dataCliente;

    @Autowired
    private FacturaRepository dataFactura;

    @GetMapping("/cliente")
    public List<Cliente> all() {
        return dataCliente.findAll();
    }

    @GetMapping("/cliente/{id}")
    public Cliente show(@PathVariable int id) {
        return buscar(id);
    }

    @GetMapping("/cliente/{id}/facturas")
    public List<Factura> facturas(@PathVariable int id) {
        buscar(id);
        return dataFactura.findByClienteClienteId(id);
    }

    @PostMapping("/cliente")
    @ResponseStatus(HttpStatus.CREATED)
    public Cliente store(@Valid @RequestBody Cliente cliente) {
        return dataCliente.save(cliente);
    }

    @PutMapping("/cliente/{id}")
    public Cliente update(@PathVariable int id, @Valid @RequestBody Cliente datos) {
        Cliente cliente = buscar(id);
        if (datos.getTipoDocumento() != null) cliente.setTipoDocumento(datos.getTipoDocumento());
        cliente.setNumeroDocumento(datos.getNumeroDocumento());
        cliente.setNombre(datos.getNombre());
        cliente.setApellido(datos.getApellido());
        cliente.setTelefono(datos.getTelefono());
        cliente.setEmail(datos.getEmail());
        cliente.setDireccion(datos.getDireccion());
        if (datos.getCiudad() != null) cliente.setCiudad(datos.getCiudad());
        return dataCliente.save(cliente);
    }

    @DeleteMapping("/cliente/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void destroy(@PathVariable int id) {
        buscar(id);
        try {
            dataCliente.deleteById(id);
        } catch (DataIntegrityViolationException e) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "El cliente tiene facturas");
        }
    }

    private Cliente buscar(int id) {
        return dataCliente.findById(id)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Cliente no encontrado"));
    }
}
