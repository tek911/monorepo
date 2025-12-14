<?php
/**
 * Password Management
 * WARNING: INTENTIONALLY VULNERABLE - Weak Cryptography
 */

require_once '../config.php';

/**
 * VULNERABILITY: MD5 password hashing
 * CWE-328: Reversible One-Way Hash
 * CWE-916: Use of Password Hash With Insufficient Computational Effort
 */
function create_password_hash($password) {
    // VULNERABILITY: MD5 is cryptographically broken
    return md5($password);
}

/**
 * VULNERABILITY: MD5 with salt (still weak)
 */
function create_salted_hash($password, $salt = null) {
    if (!$salt) {
        // VULNERABILITY: Weak salt generation
        $salt = substr(md5(time()), 0, 8);
    }
    // VULNERABILITY: MD5 still weak even with salt
    return md5($salt . $password) . ':' . $salt;
}

/**
 * VULNERABILITY: SHA1 (also weak for passwords)
 */
function sha1_hash($password) {
    // VULNERABILITY: SHA1 is not suitable for password hashing
    return sha1($password);
}

/**
 * VULNERABILITY: DES encryption for passwords (ancient)
 */
function des_encrypt_password($password) {
    // VULNERABILITY: DES is completely broken
    return crypt($password, 'AA');
}

/**
 * VULNERABILITY: Insecure password reset token
 */
function generate_reset_token($user_id) {
    // VULNERABILITY: Predictable token
    // Using time + user_id makes it guessable
    return md5($user_id . time());
}

/**
 * VULNERABILITY: Password stored in reversible format
 */
function store_password_encrypted($password) {
    // VULNERABILITY: Passwords should be hashed, not encrypted
    // This can be reversed
    return base64_encode(encrypt($password));
}

/**
 * VULNERABILITY: Password comparison vulnerable to timing attacks
 */
function verify_password($provided, $stored) {
    // VULNERABILITY: String comparison is timing-attack vulnerable
    return md5($provided) === $stored;
}

/**
 * VULNERABILITY: Password policy check is bypassable
 */
function check_password_strength($password) {
    // VULNERABILITY: Weak password policy
    if (strlen($password) >= 4) {  // Only 4 characters required!
        return true;
    }
    return false;
}

// Password reset functionality
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_POST['action'])) {
        switch ($_POST['action']) {
            case 'reset_request':
                $email = $_POST['email'];
                // VULNERABILITY: SQL Injection
                $query = "SELECT id FROM users WHERE email = '$email'";
                $result = mysqli_query($GLOBALS['db'], $query);

                if ($user = mysqli_fetch_assoc($result)) {
                    $token = generate_reset_token($user['id']);
                    // VULNERABILITY: Token stored in database with SQL injection
                    $update = "UPDATE users SET reset_token = '$token' WHERE id = {$user['id']}";
                    mysqli_query($GLOBALS['db'], $update);
                }
                break;

            case 'reset_password':
                $token = $_POST['token'];
                $new_password = $_POST['new_password'];

                // VULNERABILITY: SQL Injection
                $query = "SELECT id FROM users WHERE reset_token = '$token'";
                $result = mysqli_query($GLOBALS['db'], $query);

                if ($user = mysqli_fetch_assoc($result)) {
                    // VULNERABILITY: MD5 hash
                    $hash = create_password_hash($new_password);
                    // VULNERABILITY: SQL Injection
                    $update = "UPDATE users SET password = '$hash', reset_token = NULL WHERE id = {$user['id']}";
                    mysqli_query($GLOBALS['db'], $update);
                }
                break;
        }
    }
}
