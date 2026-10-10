package Paredes.Celis.AppVentas.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;
import Paredes.Celis.AppVentas.model.Comercial;
import Paredes.Celis.AppVentas.repository.ComercialRepository;

import java.util.List;

@RestController
@RequestMapping("api")
public class ComercialController {

    @Autowired
    private ComercialRepository dataComercial;

    @GetMapping("/comercial")
    public List<Comercial> all() {
        return dataComercial.findAll();
    }

    @GetMapping("/comercial/{id}")
    public Comercial show(@PathVariable int id) {
        return buscar(id);
    }

    @PostMapping("/comercial")
    public Comercial store(@RequestBody Comercial comercial) {
        return dataComercial.save(comercial);
    }

    @PutMapping("/comercial/{id}")
    public Comercial update(@PathVariable int id, @RequestBody Comercial datos) {
        Comercial comercial = buscar(id);
        comercial.setNombre(datos.getNombre());
        comercial.setApellido1(datos.getApellido1());
        comercial.setApellido2(datos.getApellido2());
        comercial.setComision(datos.getComision());
        return dataComercial.save(comercial);
    }

    @DeleteMapping("/comercial/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void destroy(@PathVariable int id) {
        buscar(id);
        try {
            dataComercial.deleteById(id);
        } catch (DataIntegrityViolationException e) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "El comercial tiene pedidos");
        }
    }

    private Comercial buscar(int id) {
        return dataComercial.findById(id)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Comercial no encontrado"));
    }
}
