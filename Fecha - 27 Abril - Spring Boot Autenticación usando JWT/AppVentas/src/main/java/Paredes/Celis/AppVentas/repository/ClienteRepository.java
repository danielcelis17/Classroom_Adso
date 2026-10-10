package Paredes.Celis.AppVentas.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.repository.query.Param;
import Paredes.Celis.AppVentas.model.Cliente;

import java.util.List;

public interface ClienteRepository extends JpaRepository<Cliente, Integer> {
    List<Cliente> findByNombre(@Param("nombre") String nombre);
}
