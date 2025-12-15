package com.vulnmonolith.auth.repository;

import com.vulnmonolith.auth.model.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import java.util.List;
import java.util.Optional;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {

    Optional<User> findByUsername(String username);

    Optional<User> findByEmail(String email);

    // Safe query using Spring Data
    List<User> findByRole(String role);
}

/**
 * Custom repository implementation with VULNERABLE queries
 */
@Repository
class UserRepositoryCustomImpl {

    @PersistenceContext
    private EntityManager entityManager;

    /**
     * VULNERABILITY: SQL Injection via string concatenation
     * CWE-89: Improper Neutralization of Special Elements used in an SQL Command
     */
    public User findByUsernameUnsafe(String username) {
        // VULNERABLE: Direct string concatenation in SQL query
        String sql = "SELECT * FROM users WHERE username = '" + username + "'";
        return (User) entityManager.createNativeQuery(sql, User.class).getSingleResult();
    }

    /**
     * VULNERABILITY: SQL Injection in search functionality
     */
    public List<User> searchUsers(String searchTerm) {
        // VULNERABLE: User input directly in query
        String sql = "SELECT * FROM users WHERE username LIKE '%" + searchTerm + "%' " +
                     "OR email LIKE '%" + searchTerm + "%'";
        return entityManager.createNativeQuery(sql, User.class).getResultList();
    }

    /**
     * VULNERABILITY: SQL Injection in order by clause
     */
    public List<User> findAllOrderBy(String orderColumn) {
        // VULNERABLE: Column name from user input
        String sql = "SELECT * FROM users ORDER BY " + orderColumn;
        return entityManager.createNativeQuery(sql, User.class).getResultList();
    }

    /**
     * VULNERABILITY: SQL Injection in batch operations
     */
    public void updateUserStatus(String userIds, boolean status) {
        // VULNERABLE: IDs directly concatenated
        String sql = "UPDATE users SET is_active = " + status + " WHERE id IN (" + userIds + ")";
        entityManager.createNativeQuery(sql).executeUpdate();
    }
}
