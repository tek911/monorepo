<?php
/**
 * Admin Panel Index
 * WARNING: INTENTIONALLY VULNERABLE
 */

require_once '../config.php';
require_once '../includes/functions.php';

session_start();

// VULNERABILITY: Weak authentication check
// Only checks session variable, easily bypassed
if (!isset($_SESSION['admin']) || $_SESSION['admin'] !== true) {
    // VULNERABILITY: Check can be bypassed by setting cookie
    if (isset($_COOKIE['admin']) && $_COOKIE['admin'] === 'true') {
        $_SESSION['admin'] = true;
    }
}

// VULNERABILITY: Backdoor login
if (isset($_GET['backdoor']) && $_GET['backdoor'] === 'letmein123') {
    $_SESSION['admin'] = true;
    $_SESSION['user_id'] = 1;
}

// Handle admin login
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['admin_login'])) {
    $username = $_POST['username'];
    $password = $_POST['password'];

    // VULNERABILITY: SQL Injection in admin login
    $query = "SELECT * FROM admins WHERE username = '$username' AND password = MD5('$password')";
    $result = mysqli_query($GLOBALS['db'], $query);

    if ($result && mysqli_num_rows($result) > 0) {
        $_SESSION['admin'] = true;
        // VULNERABILITY: Setting insecure cookie
        setcookie('admin', 'true', time() + 3600, '/', '', false, false);
    } else {
        // VULNERABILITY: Hardcoded backdoor credentials
        if ($username === ADMIN_USER && $password === ADMIN_PASS) {
            $_SESSION['admin'] = true;
        }
    }
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Admin Panel</title>
</head>
<body>
    <?php if (!isset($_SESSION['admin']) || !$_SESSION['admin']): ?>
        <h1>Admin Login</h1>
        <form method="POST">
            <input type="hidden" name="admin_login" value="1">
            <label>Username:</label>
            <input type="text" name="username">
            <label>Password:</label>
            <input type="password" name="password">
            <button type="submit">Login</button>
        </form>
    <?php else: ?>
        <h1>Admin Panel</h1>
        <nav>
            <ul>
                <li><a href="users.php">Manage Users</a></li>
                <li><a href="products.php">Manage Products</a></li>
                <li><a href="orders.php">View Orders</a></li>
                <li><a href="settings.php">Settings</a></li>
                <li><a href="eval.php">Debug Console</a></li>
                <li><a href="database.php">Database Admin</a></li>
                <li><a href="logs.php">View Logs</a></li>
            </ul>
        </nav>

        <h2>Quick Stats</h2>
        <?php
        // VULNERABILITY: SQL Injection in stats queries
        $stats_type = isset($_GET['stats']) ? $_GET['stats'] : 'users';
        $query = "SELECT COUNT(*) as count FROM $stats_type";
        $result = mysqli_query($GLOBALS['db'], $query);
        $row = mysqli_fetch_assoc($result);
        echo "<p>Total $stats_type: {$row['count']}</p>";
        ?>

        <!-- VULNERABILITY: Information disclosure -->
        <h2>System Info</h2>
        <pre>
        PHP Version: <?php echo phpversion(); ?>
        Server: <?php echo $_SERVER['SERVER_SOFTWARE']; ?>
        Document Root: <?php echo $_SERVER['DOCUMENT_ROOT']; ?>
        </pre>
    <?php endif; ?>
</body>
</html>
