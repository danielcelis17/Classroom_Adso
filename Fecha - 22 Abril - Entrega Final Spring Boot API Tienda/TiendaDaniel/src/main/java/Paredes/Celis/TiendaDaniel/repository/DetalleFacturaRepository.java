package Paredes.Celis.TiendaDaniel.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import Paredes.Celis.TiendaDaniel.model.DetalleFactura;

import java.util.List;

public interface DetalleFacturaRepository extends JpaRepository<DetalleFactura, Integer> {
    List<DetalleFactura> findByFacturaFacturaId(int facturaId);
}
