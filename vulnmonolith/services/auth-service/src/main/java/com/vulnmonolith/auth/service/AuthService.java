package com.vulnmonolith.auth.service;

import com.vulnmonolith.auth.config.JwtConfig;
import com.vulnmonolith.auth.model.User;
import com.vulnmonolith.auth.util.PasswordUtils;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

@Service
public class AuthService {

    @Autowired
    private JwtConfig jwtConfig;

    @PersistenceContext
    private EntityManager entityManager;

    /**
     * VULNERABILITY: SQL Injection in authentication logic
     */
    public User authenticate(String username, String password) {
        // VULNERABILITY: SQL Injection
        String hashedPassword = PasswordUtils.hashPassword(password);
        String query = "SELECT * FROM users WHERE username = '" + username +
                      "' AND password = '" + hashedPassword + "' AND is_active = true";

        try {
            return (User) entityManager.createNativeQuery(query, User.class).getSingleResult();
        } catch (Exception e) {
            return null;
        }
    }

    /**
     * Generate JWT token
     * VULNERABILITY: Uses hardcoded weak secret from config
     */
    public String generateToken(User user) {
        Map<String, Object> claims = new HashMap<>();
        claims.put("userId", user.getId());
        claims.put("username", user.getUsername());
        claims.put("role", user.getRole());
        // VULNERABILITY: Including sensitive data in JWT
        claims.put("email", user.getEmail());

        return Jwts.builder()
                .setClaims(claims)
                .setSubject(user.getUsername())
                .setIssuedAt(new Date())
                // VULNERABILITY: Token never expires (extremely long expiration)
                .setExpiration(new Date(System.currentTimeMillis() + 365L * 24 * 60 * 60 * 1000))
                // VULNERABILITY: Weak algorithm and hardcoded secret
                .signWith(SignatureAlgorithm.HS256, jwtConfig.getSecret())
                .compact();
    }

    /**
     * VULNERABILITY: Token validation with algorithm confusion potential
     */
    public boolean validateToken(String token) {
        try {
            Jwts.parser()
                .setSigningKey(jwtConfig.getSecret())
                .parseClaimsJws(token);
            return true;
        } catch (Exception e) {
            return false;
        }
    }

    /**
     * VULNERABILITY: SQL Injection in role check
     */
    public boolean hasRole(Long userId, String role) {
        // VULNERABILITY: SQL Injection
        String query = "SELECT COUNT(*) FROM users WHERE id = " + userId + " AND role = '" + role + "'";
        try {
            Number count = (Number) entityManager.createNativeQuery(query).getSingleResult();
            return count.intValue() > 0;
        } catch (Exception e) {
            return false;
        }
    }
}
