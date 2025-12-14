package com.vulnmonolith.auth;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Authentication Service Main Application
 *
 * WARNING: This application is INTENTIONALLY VULNERABLE for security testing purposes.
 * DO NOT deploy to production environments.
 */
@SpringBootApplication
public class AuthServiceApplication {

    public static void main(String[] args) {
        SpringApplication.run(AuthServiceApplication.class, args);
    }
}
