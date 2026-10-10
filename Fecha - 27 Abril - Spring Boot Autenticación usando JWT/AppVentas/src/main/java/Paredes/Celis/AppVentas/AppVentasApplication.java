package Paredes.Celis.AppVentas;

import Paredes.Celis.AppVentas.security.JWTAuthorizationFilter;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityCustomizer;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

import static org.springframework.security.config.Customizer.withDefaults;

@SpringBootApplication
public class AppVentasApplication {

	public static void main(String[] args) {
		SpringApplication.run(AppVentasApplication.class, args);
	}

	@Configuration
	@EnableWebSecurity
	public static class SecurityConfig {
		@Bean
		public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
			http
					.addFilterAfter(new JWTAuthorizationFilter(), UsernamePasswordAuthenticationFilter.class)
					.authorizeHttpRequests(auth -> auth
							.anyRequest().authenticated()
					)
					.httpBasic(withDefaults());
			return http.build();
		}

		@Bean
		public WebSecurityCustomizer webSecurityCustomizer() {
			return (web) -> web.ignoring().requestMatchers("/api/login");
		}
	}

}
