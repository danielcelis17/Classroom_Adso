package Paredes.Celis.AppVentas.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import Paredes.Celis.AppVentas.model.Usuario;

public interface UsuarioRepository extends JpaRepository<Usuario, Long> {
    public Usuario findByUsernameAndPassword(String username, String password);
}
