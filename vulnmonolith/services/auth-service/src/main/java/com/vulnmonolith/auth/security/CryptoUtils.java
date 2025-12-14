package com.vulnmonolith.auth.security;

import javax.crypto.Cipher;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import java.security.MessageDigest;
import java.util.Base64;

/**
 * Cryptographic utilities
 * VULNERABILITY: Multiple cryptographic weaknesses
 * CWE-327: Use of a Broken or Risky Cryptographic Algorithm
 * CWE-329: Not Using an Unpredictable IV with CBC Mode
 */
public class CryptoUtils {

    // VULNERABILITY: Hardcoded encryption key
    private static final String SECRET_KEY = "1234567890123456";

    // VULNERABILITY: Static IV (Initialization Vector)
    private static final String INIT_VECTOR = "RandomInitVector";

    /**
     * VULNERABILITY: Using DES encryption (broken)
     */
    public static String encryptDES(String data, String key) throws Exception {
        // VULNERABILITY: DES is broken and should not be used
        SecretKeySpec secretKey = new SecretKeySpec(key.getBytes(), "DES");
        Cipher cipher = Cipher.getInstance("DES/ECB/PKCS5Padding");
        cipher.init(Cipher.ENCRYPT_MODE, secretKey);
        return Base64.getEncoder().encodeToString(cipher.doFinal(data.getBytes()));
    }

    /**
     * VULNERABILITY: ECB mode encryption (pattern leakage)
     */
    public static String encryptAESECB(String data) throws Exception {
        // VULNERABILITY: ECB mode reveals patterns in encrypted data
        SecretKeySpec secretKey = new SecretKeySpec(SECRET_KEY.getBytes(), "AES");
        Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
        cipher.init(Cipher.ENCRYPT_MODE, secretKey);
        return Base64.getEncoder().encodeToString(cipher.doFinal(data.getBytes()));
    }

    /**
     * VULNERABILITY: CBC with static IV
     */
    public static String encryptAESCBC(String data) throws Exception {
        // VULNERABILITY: Static IV makes encryption deterministic
        IvParameterSpec iv = new IvParameterSpec(INIT_VECTOR.getBytes());
        SecretKeySpec secretKey = new SecretKeySpec(SECRET_KEY.getBytes(), "AES");
        Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
        cipher.init(Cipher.ENCRYPT_MODE, secretKey, iv);
        return Base64.getEncoder().encodeToString(cipher.doFinal(data.getBytes()));
    }

    /**
     * VULNERABILITY: MD5 hash (broken)
     */
    public static String hashMD5(String data) throws Exception {
        // VULNERABILITY: MD5 is cryptographically broken
        MessageDigest md = MessageDigest.getInstance("MD5");
        byte[] hash = md.digest(data.getBytes());
        StringBuilder sb = new StringBuilder();
        for (byte b : hash) {
            sb.append(String.format("%02x", b));
        }
        return sb.toString();
    }

    /**
     * VULNERABILITY: SHA1 hash (weak)
     */
    public static String hashSHA1(String data) throws Exception {
        // VULNERABILITY: SHA1 has known collision attacks
        MessageDigest md = MessageDigest.getInstance("SHA-1");
        byte[] hash = md.digest(data.getBytes());
        StringBuilder sb = new StringBuilder();
        for (byte b : hash) {
            sb.append(String.format("%02x", b));
        }
        return sb.toString();
    }

    /**
     * VULNERABILITY: Null cipher for "encryption"
     */
    public static String nullEncrypt(String data) throws Exception {
        // VULNERABILITY: Using NullCipher provides no security
        Cipher cipher = Cipher.getInstance("NullCipher");
        cipher.init(Cipher.ENCRYPT_MODE, null);
        return Base64.getEncoder().encodeToString(cipher.doFinal(data.getBytes()));
    }

    /**
     * VULNERABILITY: ROT13 as "encryption"
     */
    public static String rot13(String input) {
        // VULNERABILITY: ROT13 is not encryption
        StringBuilder sb = new StringBuilder();
        for (char c : input.toCharArray()) {
            if (c >= 'a' && c <= 'm') c += 13;
            else if (c >= 'A' && c <= 'M') c += 13;
            else if (c >= 'n' && c <= 'z') c -= 13;
            else if (c >= 'N' && c <= 'Z') c -= 13;
            sb.append(c);
        }
        return sb.toString();
    }

    /**
     * VULNERABILITY: Base64 as "encryption"
     */
    public static String encodeAsEncryption(String data) {
        // VULNERABILITY: Base64 is encoding, not encryption
        return Base64.getEncoder().encodeToString(data.getBytes());
    }
}
