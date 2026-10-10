package Paredes.Celis.AppVentas.controller;

import io.jsonwebtoken.Jwts;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.AuthorityUtils;
import org.springframework.web.bind.annotation.*;
import Paredes.Celis.AppVentas.model.LoginUser;
import Paredes.Celis.AppVentas.model.Usuario;
import Paredes.Celis.AppVentas.repository.UsuarioRepository;
import Paredes.Celis.AppVentas.security.JWTAuthorizationFilter;

import java.security.Key;
import java.util.Date;
import java.util.List;
import java.util.stream.Collectors;

@RestController
@RequestMapping("api")
public class UsuarioController {
    @Autowired
    private UsuarioRepository usuarioRepository;

    @PostMapping("/login")
    public Usuario login(@RequestBody LoginUser user) {
        String token = getJWTToken(user.getUsername());
        Usuario usuario = usuarioRepository.findByUsernameAndPassword(user.getUsername(), user.getPassword());
        if (usuario != null) {
            usuario.setToken(token);
            return usuario;
        }
        return null;
    }

    @PostMapping("/usuario")
    public Usuario addUsuario(@RequestBody Usuario usuario) {
        return usuarioRepository.save(usuario);
    }

    private String getJWTToken(String username) {
        Key key = JWTAuthorizationFilter.key;
        List<GrantedAuthority> grantedAuthorities = AuthorityUtils
                .commaSeparatedStringToAuthorityList("ROLE_USER");

        String token = Jwts
                .builder()
                .setId("softtekJWT")
                .setSubject(username)
                .claim("authorities",
                        grantedAuthorities.stream()
                                .map(GrantedAuthority::getAuthority)
                                .collect(Collectors.toList()))
                .setIssuedAt(new Date(System.currentTimeMillis()))
                .setExpiration(new Date(System.currentTimeMillis() + 600000))
                .signWith(key).compact();

        return "Bearer " + token;
    }
}
