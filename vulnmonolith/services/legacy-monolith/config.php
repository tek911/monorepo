<?php
/**
 * Configuration file for Legacy Monolith
 * WARNING: INTENTIONALLY VULNERABLE - DO NOT USE IN PRODUCTION
 *
 * VULNERABILITY: Hardcoded credentials throughout
 * CWE-798: Use of Hard-coded Credentials
 */

// VULNERABILITY: Debug mode enabled
error_reporting(E_ALL);
ini_set('display_errors', 1);

// VULNERABILITY: Hardcoded database credentials
define('DB_HOST', 'localhost');
define('DB_USER', 'root');
define('DB_PASS', 'P@ssw0rd123!');
define('DB_NAME', 'legacy_app');

// VULNERABILITY: Hardcoded encryption key
define('ENCRYPTION_KEY', 'super-secret-key-12345');

// VULNERABILITY: Hardcoded API keys
define('STRIPE_SECRET_KEY', 'sk_test_FAKEFAKEFAKEFAKE_NOTREAL');
define('SENDGRID_API_KEY', 'SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx');

// VULNERABILITY: Hardcoded admin credentials
define('ADMIN_USER', 'admin');
define('ADMIN_PASS', 'admin123');

// VULNERABILITY: Hardcoded AWS credentials
define('AWS_ACCESS_KEY', 'AKIAIOSFODNN7EXAMPLE');
define('AWS_SECRET_KEY', 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY');

// VULNERABILITY: Weak session configuration
ini_set('session.use_only_cookies', 0);
ini_set('session.cookie_httponly', 0);
ini_set('session.cookie_secure', 0);

// VULNERABILITY: File upload settings too permissive
define('UPLOAD_DIR', '/var/www/uploads/');
define('MAX_UPLOAD_SIZE', 100 * 1024 * 1024); // 100MB

// VULNERABILITY: Magic quotes assumption (deprecated)
// Some old code may rely on magic_quotes_gpc being ON

// Database connection
$db_connection = null;

function db_connect() {
    global $db_connection;
    // VULNERABILITY: Using deprecated mysql_* functions concept
    // (Would use mysqli in actual PHP 7+ but showing the pattern)
    $db_connection = mysqli_connect(DB_HOST, DB_USER, DB_PASS, DB_NAME);
    if (!$db_connection) {
        // VULNERABILITY: Error message exposes database info
        die("Database connection failed: " . mysqli_connect_error());
    }
    return $db_connection;
}

// VULNERABILITY: Global variables
$GLOBALS['db'] = db_connect();
$GLOBALS['user'] = null;
$GLOBALS['admin'] = false;
