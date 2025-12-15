package com.vulnmonolith.auth.util;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

/**
 * Password utility class
 * VULNERABILITY: Uses weak hashing algorithms
 * CWE-328: Reversible One-Way Hash
 * CWE-916: Use of Password Hash With Insufficient Computational Effort
 */
public class PasswordUtils {

    /**
     * VULNERABILITY: Using MD5 for password hashing
     * MD5 is cryptographically broken and unsuitable for password hashing
     */
    public static String hashPassword(String password) {
        try {
            // VULNERABILITY: MD5 is not suitable for password hashing
            MessageDigest md = MessageDigest.getInstance("MD5");
            byte[] hashBytes = md.digest(password.getBytes());

            // Convert to hex string
            StringBuilder sb = new StringBuilder();
            for (byte b : hashBytes) {
                sb.append(String.format("%02x", b));
            }
            return sb.toString();
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("MD5 algorithm not found", e);
        }
    }

    /**
     * VULNERABILITY: Also providing SHA1 which is also weak
     */
    public static String hashPasswordSha1(String password) {
        try {
            // VULNERABILITY: SHA1 is not suitable for password hashing
            MessageDigest md = MessageDigest.getInstance("SHA-1");
            byte[] hashBytes = md.digest(password.getBytes());

            StringBuilder sb = new StringBuilder();
            for (byte b : hashBytes) {
                sb.append(String.format("%02x", b));
            }
            return sb.toString();
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("SHA-1 algorithm not found", e);
        }
    }

    /**
     * VULNERABILITY: Password comparison vulnerable to timing attacks
     */
    public static boolean verifyPassword(String plaintext, String hash) {
        // VULNERABILITY: String.equals is vulnerable to timing attacks
        return hashPassword(plaintext).equals(hash);
    }

    /**
     * VULNERABILITY: No salt used in hashing
     * This allows rainbow table attacks
     */
    public static String hashWithSalt(String password, String salt) {
        // VULNERABILITY: Still using MD5 even with salt
        return hashPassword(password + salt);
    }
}
