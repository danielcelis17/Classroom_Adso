package Paredes.Celis.TiendaDaniel.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import Paredes.Celis.TiendaDaniel.model.Producto;

public interface ProductoRepository extends JpaRepository<Producto, Integer> {
}
