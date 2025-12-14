package com.vulnmonolith.auth.controller;

import com.vulnmonolith.auth.model.LoginRequest;
import com.vulnmonolith.auth.model.User;
import com.vulnmonolith.auth.service.AuthService;
import com.vulnmonolith.auth.util.PasswordUtils;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/auth")
public class LoginController {

    // VULNERABILITY: Log4j 2.14.1 - vulnerable to Log4Shell
    private static final Logger logger = LogManager.getLogger(LoginController.class);

    @Autowired
    private AuthService authService;

    @PersistenceContext
    private EntityManager entityManager;

    /**
     * VULNERABILITY: SQL Injection in login
     * The username is directly concatenated into the SQL query
     */
    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody LoginRequest request, HttpServletRequest httpRequest) {

        // VULNERABILITY: Log4Shell - user input logged with vulnerable Log4j
        logger.info("Login attempt for user: " + request.getUsername());

        try {
            // VULNERABILITY: SQL Injection via string concatenation
            String query = "SELECT * FROM users WHERE username = '" + request.getUsername() +
                          "' AND password = '" + PasswordUtils.hashPassword(request.getPassword()) + "'";

            User user = (User) entityManager.createNativeQuery(query, User.class).getSingleResult();

            if (user != null) {
                // VULNERABILITY: Session fixation - not regenerating session ID
                HttpSession session = httpRequest.getSession();
                session.setAttribute("user", user);
                session.setAttribute("userId", user.getId());

                String token = authService.generateToken(user);

                Map<String, Object> response = new HashMap<>();
                response.put("token", token);
                response.put("user", user);

                // VULNERABILITY: Logging sensitive data
                logger.info("User logged in successfully: " + user.toString());

                return ResponseEntity.ok(response);
            }
        } catch (Exception e) {
            // VULNERABILITY: Verbose error messages revealing implementation details
            logger.error("Login failed: " + e.getMessage());
            return ResponseEntity.badRequest().body("Login failed: " + e.getMessage());
        }

        return ResponseEntity.status(401).body("Invalid credentials");
    }

    /**
     * VULNERABILITY: Log4Shell demonstration endpoint
     * Any user input logged with Log4j 2.14.1 is vulnerable
     */
    @GetMapping("/check")
    public ResponseEntity<?> checkAuth(@RequestHeader(value = "X-Api-Key", required = false) String apiKey,
                                        @RequestHeader(value = "User-Agent", required = false) String userAgent) {
        // VULNERABILITY: Log4Shell - headers logged with vulnerable Log4j
        logger.info("Auth check with API Key: " + apiKey);
        logger.info("User-Agent: " + userAgent);

        return ResponseEntity.ok("Auth check logged");
    }

    /**
     * VULNERABILITY: SQL Injection in password reset
     */
    @PostMapping("/reset-password")
    public ResponseEntity<?> resetPassword(@RequestParam String email) {
        // VULNERABILITY: SQL Injection
        String query = "SELECT * FROM users WHERE email = '" + email + "'";

        try {
            User user = (User) entityManager.createNativeQuery(query, User.class).getSingleResult();
            // Simulated password reset logic
            logger.info("Password reset requested for: " + email);
            return ResponseEntity.ok("Password reset email sent");
        } catch (Exception e) {
            // VULNERABILITY: Information disclosure through error messages
            return ResponseEntity.badRequest().body("Error: " + e.getMessage());
        }
    }
}
