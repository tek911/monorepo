package com.vulnmonolith.testfixtures;

/**
 * Hardcoded Secrets Test File
 * INTENTIONAL vulnerabilities for testing secret detection tools.
 * These should be EXCLUDED from security scan results.
 */
public class HardcodedSecretsTest {

    // INTENTIONAL: Test AWS credentials detection
    private static final String AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE";
    private static final String AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY";

    // INTENTIONAL: Test API key detection
    private static final String STRIPE_API_KEY = "sk_test_FAKE_KEY_FOR_TESTING_ONLY_1234";
    private static final String SENDGRID_API_KEY = "SG.FAKE_SENDGRID_KEY_FOR_TESTING_ONLY";

    // INTENTIONAL: Test database credentials detection
    private static final String DB_PASSWORD = "super_secret_password_123!";
    private static final String DB_CONNECTION = "postgres://admin:password123@localhost:5432/production";

    // INTENTIONAL: Test OAuth tokens
    private static final String GITHUB_TOKEN = "ghp_FAKE_TOKEN_FOR_TESTING_ONLY_xxxxx";
    private static final String SLACK_TOKEN = "xoxb-fake-slack-token-for-testing-only";

    // INTENTIONAL: Test private keys
    private static final String PRIVATE_KEY = """
        -----BEGIN RSA PRIVATE KEY-----
        MIIEowIBAAKCAQEA0Z3VS5JJcds3xfn/ygWyF8PbnGy0AHB7MAsAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAfake+key+for+testing+only+AAAA
        -----END RSA PRIVATE KEY-----
        """;

    // INTENTIONAL: Test JWT secrets
    private static final String JWT_SECRET = "my-super-secret-jwt-key-that-should-be-detected";

    /**
     * INTENTIONALLY connects with hardcoded credentials.
     * Used to test that security controls catch this pattern.
     */
    public void connectWithHardcodedCredentials() {
        String connectionString = "mongodb://root:toor@localhost:27017/admin";
        // INTENTIONAL - would connect with hardcoded creds
        System.out.println("Connecting to: " + connectionString);
    }

    /**
     * INTENTIONALLY uses API key inline.
     * Tests detection of inline secrets.
     */
    public void callApiWithInlineKey() {
        String apiKey = "api_key_1234567890abcdef";
        // INTENTIONAL - passes secret as parameter
        System.out.println("Using API key: " + apiKey);
    }

    /**
     * INTENTIONALLY returns sensitive configuration.
     * Tests detection of secrets in return values.
     */
    public String getSensitiveConfig() {
        // INTENTIONAL - returns hardcoded secrets
        return String.format(
            "AWS_KEY=%s, SECRET=%s, PASSWORD=%s",
            AWS_ACCESS_KEY, AWS_SECRET_KEY, DB_PASSWORD
        );
    }
}
