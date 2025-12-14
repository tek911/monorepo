package com.vulnmonolith.auth.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;

import java.util.Arrays;

/**
 * Security Configuration
 * VULNERABILITY: Overly permissive security settings
 */
@Configuration
@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
            // VULNERABILITY: CSRF protection disabled
            .csrf().disable()

            // VULNERABILITY: All endpoints publicly accessible
            .authorizeRequests()
                .antMatchers("/**").permitAll()

            // VULNERABILITY: Frame options disabled (clickjacking)
            .and()
            .headers()
                .frameOptions().disable()
                // VULNERABILITY: XSS protection disabled
                .xssProtection().disable()
                // VULNERABILITY: Content type sniffing protection disabled
                .contentTypeOptions().disable()

            // VULNERABILITY: CORS configured to allow all origins
            .and()
            .cors();
    }

    /**
     * VULNERABILITY: CORS allows all origins
     */
    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration configuration = new CorsConfiguration();
        // VULNERABILITY: Allows any origin
        configuration.setAllowedOrigins(Arrays.asList("*"));
        // VULNERABILITY: Allows all methods
        configuration.setAllowedMethods(Arrays.asList("*"));
        // VULNERABILITY: Allows all headers
        configuration.setAllowedHeaders(Arrays.asList("*"));
        // VULNERABILITY: Allows credentials with wildcard origin
        configuration.setAllowCredentials(true);

        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", configuration);
        return source;
    }
}
