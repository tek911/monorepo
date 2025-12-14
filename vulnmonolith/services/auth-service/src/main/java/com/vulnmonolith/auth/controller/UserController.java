package com.vulnmonolith.auth.controller;

import com.vulnmonolith.auth.model.User;
import com.vulnmonolith.auth.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/users")
public class UserController {

    @Autowired
    private UserRepository userRepository;

    @PersistenceContext
    private EntityManager entityManager;

    /**
     * VULNERABILITY: IDOR (Insecure Direct Object Reference)
     * No authorization check - any user can access any profile
     * CWE-639: Authorization Bypass Through User-Controlled Key
     */
    @GetMapping("/{userId}")
    public ResponseEntity<?> getUserProfile(@PathVariable Long userId) {
        // VULNERABILITY: No check if requesting user is authorized to view this profile
        Optional<User> user = userRepository.findById(userId);

        if (user.isPresent()) {
            // VULNERABILITY: Returning sensitive data (SSN, credit card)
            return ResponseEntity.ok(user.get());
        }

        return ResponseEntity.notFound().build();
    }

    /**
     * VULNERABILITY: IDOR in profile update
     * Any authenticated user can update any other user's profile
     */
    @PutMapping("/{userId}")
    public ResponseEntity<?> updateUserProfile(@PathVariable Long userId, @RequestBody User updatedUser) {
        // VULNERABILITY: No authorization check
        Optional<User> existingUser = userRepository.findById(userId);

        if (existingUser.isPresent()) {
            User user = existingUser.get();
            user.setEmail(updatedUser.getEmail());
            user.setUsername(updatedUser.getUsername());
            // VULNERABILITY: Mass assignment - role can be changed by user
            if (updatedUser.getRole() != null) {
                user.setRole(updatedUser.getRole());
            }
            userRepository.save(user);
            return ResponseEntity.ok(user);
        }

        return ResponseEntity.notFound().build();
    }

    /**
     * VULNERABILITY: SQL Injection in search
     */
    @GetMapping("/search")
    public ResponseEntity<?> searchUsers(@RequestParam String q) {
        // VULNERABILITY: SQL Injection via string concatenation
        String query = "SELECT * FROM users WHERE username LIKE '%" + q + "%' OR email LIKE '%" + q + "%'";
        List<User> users = entityManager.createNativeQuery(query, User.class).getResultList();
        return ResponseEntity.ok(users);
    }

    /**
     * VULNERABILITY: SQL Injection in sorting
     */
    @GetMapping("/list")
    public ResponseEntity<?> listUsers(
            @RequestParam(defaultValue = "id") String sortBy,
            @RequestParam(defaultValue = "ASC") String order) {
        // VULNERABILITY: Column name and order from user input
        String query = "SELECT * FROM users ORDER BY " + sortBy + " " + order;
        List<User> users = entityManager.createNativeQuery(query, User.class).getResultList();
        return ResponseEntity.ok(users);
    }

    /**
     * VULNERABILITY: Batch operation with SQL Injection
     */
    @PostMapping("/batch-delete")
    public ResponseEntity<?> batchDeleteUsers(@RequestBody String userIds) {
        // VULNERABILITY: User IDs directly in query
        String query = "DELETE FROM users WHERE id IN (" + userIds + ")";
        int deleted = entityManager.createNativeQuery(query).executeUpdate();
        return ResponseEntity.ok("Deleted " + deleted + " users");
    }

    /**
     * VULNERABILITY: IDOR + Information Disclosure
     * Exposes all user details including sensitive data
     */
    @GetMapping("/{userId}/details")
    public ResponseEntity<?> getUserDetails(@PathVariable Long userId) {
        // VULNERABILITY: No authorization, returns sensitive data
        String query = "SELECT id, username, email, ssn, credit_card, api_key FROM users WHERE id = " + userId;
        Object result = entityManager.createNativeQuery(query).getSingleResult();
        return ResponseEntity.ok(result);
    }
}
