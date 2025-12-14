package com.vulnmonolith.auth.util;

import java.util.Random;
import java.util.UUID;

/**
 * Token generation utilities
 * VULNERABILITY: Uses insecure random number generation
 * CWE-330: Use of Insufficiently Random Values
 */
public class TokenGenerator {

    // VULNERABILITY: Using java.util.Random instead of SecureRandom
    private static final Random random = new Random();

    /**
     * VULNERABILITY: Insecure token generation using predictable Random
     */
    public static String generateToken() {
        // VULNERABILITY: java.util.Random is predictable
        StringBuilder token = new StringBuilder();
        String chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

        for (int i = 0; i < 32; i++) {
            token.append(chars.charAt(random.nextInt(chars.length())));
        }

        return token.toString();
    }

    /**
     * VULNERABILITY: Predictable session ID generation
     */
    public static String generateSessionId() {
        // VULNERABILITY: Using timestamp + predictable random
        return System.currentTimeMillis() + "-" + random.nextInt(10000);
    }

    /**
     * VULNERABILITY: Weak API key generation
     */
    public static String generateApiKey() {
        // VULNERABILITY: Predictable pattern
        return "api_" + System.currentTimeMillis() + "_" + random.nextInt(999999);
    }

    /**
     * VULNERABILITY: Password reset token with insufficient entropy
     */
    public static String generateResetToken() {
        // VULNERABILITY: Only 6 digits - easily brute forced
        return String.format("%06d", random.nextInt(1000000));
    }

    /**
     * Slightly better but still flawed
     */
    public static String generateUuidToken() {
        // UUID.randomUUID() uses SecureRandom internally, but the implementation
        // reveals this is sometimes combined with weaker sources
        return UUID.randomUUID().toString().replace("-", "");
    }
}
