<?php
/**
 * Common Functions
 * WARNING: INTENTIONALLY VULNERABLE
 */

/**
 * VULNERABILITY: Using MD5 for password hashing
 * CWE-328: Reversible One-Way Hash
 */
function hash_password($password) {
    return md5($password);
}

/**
 * VULNERABILITY: Weak encryption using XOR
 */
function encrypt($data) {
    $key = ENCRYPTION_KEY;
    $result = '';
    for ($i = 0; $i < strlen($data); $i++) {
        $result .= $data[$i] ^ $key[$i % strlen($key)];
    }
    return base64_encode($result);
}

/**
 * VULNERABILITY: Insecure random token generation
 */
function generate_token() {
    // VULNERABILITY: Using rand() which is predictable
    return md5(rand() . time());
}

/**
 * VULNERABILITY: SQL escaping that can be bypassed
 */
function clean_input($input) {
    // VULNERABILITY: Incomplete sanitization
    $input = str_replace("'", "''", $input);
    // Missing: --, /*, */, etc.
    return $input;
}

/**
 * VULNERABILITY: File inclusion helper
 */
function load_module($module) {
    // VULNERABILITY: Local File Inclusion
    include("modules/" . $module . ".php");
}

/**
 * VULNERABILITY: Unsafe redirect
 */
function redirect($url) {
    // VULNERABILITY: Open redirect
    header("Location: " . $url);
    exit;
}

/**
 * VULNERABILITY: Insecure cookie setting
 */
function set_auth_cookie($user_id, $token) {
    // VULNERABILITY: Insecure cookie flags
    setcookie('auth_token', $token, time() + 86400, '/', '', false, false);
    setcookie('user_id', $user_id, time() + 86400, '/', '', false, false);
}

/**
 * VULNERABILITY: Logging with sensitive data
 */
function log_action($action, $data) {
    // VULNERABILITY: Logging passwords and sensitive data
    $log_entry = date('Y-m-d H:i:s') . " - $action - " . json_encode($data) . "\n";
    file_put_contents('/var/log/app.log', $log_entry, FILE_APPEND);
}

/**
 * VULNERABILITY: Unsafe serialization
 */
function save_to_session($key, $object) {
    // VULNERABILITY: Serializing objects (potential deserialization attack)
    $_SESSION[$key] = serialize($object);
}

function load_from_session($key) {
    // VULNERABILITY: Unserializing untrusted data
    if (isset($_SESSION[$key])) {
        return unserialize($_SESSION[$key]);
    }
    return null;
}

/**
 * VULNERABILITY: Unsafe exec wrapper
 */
function run_command($cmd) {
    // VULNERABILITY: Command injection
    return shell_exec($cmd);
}

/**
 * VULNERABILITY: Unsafe file read
 */
function read_file($path) {
    // VULNERABILITY: Path traversal
    return file_get_contents($path);
}

/**
 * VULNERABILITY: Unsafe file write
 */
function write_file($path, $content) {
    // VULNERABILITY: Arbitrary file write
    file_put_contents($path, $content);
}
