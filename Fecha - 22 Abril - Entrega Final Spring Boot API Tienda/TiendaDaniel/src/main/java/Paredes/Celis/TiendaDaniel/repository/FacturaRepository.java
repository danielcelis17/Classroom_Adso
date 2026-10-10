package Paredes.Celis.TiendaDaniel.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import Paredes.Celis.TiendaDaniel.model.Factura;

import java.util.List;
import java.util.Optional;

public interface FacturaRepository extends JpaRepository<Factura, Integer> {
    // Para numerar la siguiente factura (FAC-000001, FAC-000002, ...)
    Optional<Factura> findTopByOrderByFacturaIdDesc();

    List<Factura> findByClienteClienteId(int clienteId);
}
