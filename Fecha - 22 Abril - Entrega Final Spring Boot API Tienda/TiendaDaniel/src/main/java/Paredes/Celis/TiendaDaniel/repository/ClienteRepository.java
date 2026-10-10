package Paredes.Celis.TiendaDaniel.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import Paredes.Celis.TiendaDaniel.model.Cliente;

public interface ClienteRepository extends JpaRepository<Cliente, Integer> {
}
