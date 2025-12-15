package com.vulnmonolith.auth.model;

import lombok.Data;
import java.io.Serializable;

/**
 * User session object - serializable for session storage
 * VULNERABILITY: Used in insecure deserialization
 */
@Data
public class UserSession implements Serializable {

    private static final long serialVersionUID = 1L;

    private Long userId;
    private String username;
    private String role;
    private String sessionToken;
    private long createdAt;
    private long expiresAt;

    // VULNERABILITY: Custom readObject can be exploited
    private void readObject(java.io.ObjectInputStream in)
            throws java.io.IOException, ClassNotFoundException {
        in.defaultReadObject();
        // Simulated "validation" that could be bypassed
        if (this.role == null) {
            this.role = "USER";
        }
    }
}
