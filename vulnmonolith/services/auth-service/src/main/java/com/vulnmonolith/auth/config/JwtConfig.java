package com.vulnmonolith.auth.config;

import org.springframework.stereotype.Component;

/**
 * JWT Configuration
 * VULNERABILITY: Hardcoded secrets
 * CWE-798: Use of Hard-coded Credentials
 */
@Component
public class JwtConfig {

    // VULNERABILITY: Hardcoded JWT secret
    // This secret is used to sign all JWT tokens
    private static final String JWT_SECRET = "mySuper$ecretKey123!@#";

    // VULNERABILITY: Hardcoded backup key
    private static final String BACKUP_SECRET = "backupKey456$%^";

    // VULNERABILITY: Default admin credentials
    public static final String DEFAULT_ADMIN_USERNAME = "admin";
    public static final String DEFAULT_ADMIN_PASSWORD = "admin123";

    // VULNERABILITY: API key for internal services
    private static final String INTERNAL_API_KEY = "internal-api-key-do-not-share-12345";

    public String getSecret() {
        return JWT_SECRET;
    }

    public String getBackupSecret() {
        return BACKUP_SECRET;
    }

    public String getInternalApiKey() {
        return INTERNAL_API_KEY;
    }

    // VULNERABILITY: Hardcoded encryption key
    public static final byte[] ENCRYPTION_KEY = {
        0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08,
        0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10
    };

    // VULNERABILITY: Hardcoded IV (Initialization Vector)
    public static final byte[] ENCRYPTION_IV = {
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
    };
}
