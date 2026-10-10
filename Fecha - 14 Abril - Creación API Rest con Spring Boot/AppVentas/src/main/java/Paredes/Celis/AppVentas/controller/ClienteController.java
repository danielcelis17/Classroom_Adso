package Paredes.Celis.AppVentas.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
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

    @PostMapping("/cliente")
    public Cliente store(@RequestBody Cliente cliente) {
        return dataCliente.save(cliente);
    }
}
