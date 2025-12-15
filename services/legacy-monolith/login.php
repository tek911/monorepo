<?php
/**
 * Login Page
 * WARNING: INTENTIONALLY VULNERABLE
 *
 * VULNERABILITIES:
 * - SQL Injection
 * - Weak password hashing (MD5)
 * - Session fixation
 * - Credential enumeration
 */

require_once 'config.php';
require_once 'includes/functions.php';

// VULNERABILITY: Session fixation - not regenerating session ID
session_start();

$error = '';
$success = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // VULNERABILITY: Direct use of $_POST without sanitization
    $username = $_POST['username'];
    $password = $_POST['password'];

    // VULNERABILITY: MD5 password hashing (weak)
    $password_hash = md5($password);

    // VULNERABILITY: SQL Injection - string concatenation
    $query = "SELECT * FROM users WHERE username = '$username' AND password = '$password_hash'";

    // VULNERABILITY: Logging credentials
    error_log("Login attempt: $username / $password");

    $result = mysqli_query($GLOBALS['db'], $query);

    if ($result && mysqli_num_rows($result) > 0) {
        $user = mysqli_fetch_assoc($result);

        // VULNERABILITY: Not regenerating session ID (session fixation)
        $_SESSION['user_id'] = $user['id'];
        $_SESSION['username'] = $user['username'];
        $_SESSION['role'] = $user['role'];

        // VULNERABILITY: Sensitive data in session
        $_SESSION['password_hash'] = $user['password'];

        header("Location: index.php?message=Welcome, " . $username);
        exit;
    } else {
        // VULNERABILITY: User enumeration through different error messages
        $check_user = mysqli_query($GLOBALS['db'], "SELECT id FROM users WHERE username = '$username'");
        if (mysqli_num_rows($check_user) > 0) {
            $error = "Invalid password for user: $username";
        } else {
            $error = "User does not exist: $username";
        }
    }
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
</head>
<body>
    <h1>Login</h1>

    <?php if ($error): ?>
        <!-- VULNERABILITY: Reflected XSS in error message -->
        <div class="error"><?php echo $error; ?></div>
    <?php endif; ?>

    <form method="POST" action="">
        <!-- VULNERABILITY: No CSRF token -->
        <label>Username:</label>
        <input type="text" name="username" value="<?php echo @$_POST['username']; ?>">

        <label>Password:</label>
        <input type="password" name="password">

        <button type="submit">Login</button>
    </form>

    <p><a href="register.php">Create Account</a></p>
    <p><a href="forgot_password.php">Forgot Password?</a></p>

    <!-- VULNERABILITY: Debug information in production -->
    <?php if (isset($_GET['debug'])): ?>
        <pre><?php print_r($_SESSION); ?></pre>
        <pre><?php print_r($_SERVER); ?></pre>
    <?php endif; ?>
</body>
</html>
