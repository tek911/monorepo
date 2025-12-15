<?php
/**
 * Main entry point for Legacy Monolith
 * WARNING: INTENTIONALLY VULNERABLE
 */

require_once 'config.php';
require_once 'includes/functions.php';

session_start();

// VULNERABILITY: User input directly used
$page = isset($_GET['page']) ? $_GET['page'] : 'home';

// VULNERABILITY: Local File Inclusion (LFI)
// Attack: ?page=../../../etc/passwd
$template = "templates/" . $page . ".php";

if (file_exists($template)) {
    include($template);
} else {
    // VULNERABILITY: Error message reveals file system structure
    echo "Template not found: " . htmlspecialchars($template);
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Legacy Application</title>
    <!-- VULNERABILITY: jQuery 2.2.4 with XSS vulnerabilities -->
    <script src="https://code.jquery.com/jquery-2.2.4.min.js"></script>
</head>
<body>
    <header>
        <nav>
            <a href="?page=home">Home</a>
            <a href="?page=products">Products</a>
            <a href="?page=search">Search</a>
            <a href="login.php">Login</a>
            <a href="admin/index.php">Admin</a>
        </nav>
    </header>

    <main id="content">
        <?php
        // VULNERABILITY: Reflected XSS via message parameter
        if (isset($_GET['message'])) {
            echo "<div class='message'>" . $_GET['message'] . "</div>";
        }
        ?>
    </main>

    <footer>
        <?php
        // VULNERABILITY: Information disclosure
        echo "PHP Version: " . phpversion();
        echo " | Server: " . $_SERVER['SERVER_SOFTWARE'];
        ?>
    </footer>
</body>
</html>
