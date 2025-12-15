package com.vulnmonolith.auth.model;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import javax.persistence.*;
import java.io.Serializable;
import java.time.LocalDateTime;

@Entity
@Table(name = "users")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class User implements Serializable {

    private static final long serialVersionUID = 1L;

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(unique = true, nullable = false)
    private String username;

    @Column(nullable = false)
    private String email;

    // VULNERABILITY: Password stored with weak hashing (see PasswordUtils)
    @Column(nullable = false)
    private String password;

    @Column(name = "role")
    private String role = "USER";

    @Column(name = "api_key")
    private String apiKey;

    @Column(name = "created_at")
    private LocalDateTime createdAt;

    @Column(name = "last_login")
    private LocalDateTime lastLogin;

    @Column(name = "is_active")
    private boolean isActive = true;

    // VULNERABILITY: Sensitive data that could be exposed via IDOR
    @Column(name = "ssn")
    private String ssn;

    @Column(name = "credit_card")
    private String creditCard;

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
    }
}
