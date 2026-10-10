package Paredes.Celis.AppVentas.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import Paredes.Celis.AppVentas.model.Pedido;

public interface PedidoRepository extends JpaRepository<Pedido, Integer> {
}
