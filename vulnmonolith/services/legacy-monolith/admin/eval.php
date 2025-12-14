<?php
/**
 * Admin Debug/Eval Page
 * WARNING: INTENTIONALLY VULNERABLE - REMOTE CODE EXECUTION
 *
 * VULNERABILITIES:
 * - eval() with user input (RCE)
 * - No authentication
 * - Command injection
 */

require_once '../config.php';

// VULNERABILITY: No authentication check for admin page
// Anyone can access this

// VULNERABILITY: eval() with user input - Remote Code Execution
if (isset($_POST['code'])) {
    $code = $_POST['code'];

    echo "<h2>Executing PHP Code:</h2>";
    echo "<pre>";
    // VULNERABILITY: eval() executes arbitrary PHP code
    // Attack: system('id'); or file_get_contents('/etc/passwd');
    eval($code);
    echo "</pre>";
}

// VULNERABILITY: shell_exec with user input - Command Injection
if (isset($_GET['cmd'])) {
    $cmd = $_GET['cmd'];

    echo "<h2>Command Output:</h2>";
    echo "<pre>";
    // VULNERABILITY: Direct command execution
    echo shell_exec($cmd);
    echo "</pre>";
}

// VULNERABILITY: Another command injection vector
if (isset($_POST['ping'])) {
    $host = $_POST['ping'];

    echo "<h2>Ping Result:</h2>";
    echo "<pre>";
    // VULNERABILITY: Command injection via ping
    // Attack: host=127.0.0.1; cat /etc/passwd
    system("ping -c 4 " . $host);
    echo "</pre>";
}

// VULNERABILITY: exec() with user input
if (isset($_GET['exec'])) {
    $output = array();
    // VULNERABILITY: Command injection
    exec($_GET['exec'], $output);
    echo "<pre>" . implode("\n", $output) . "</pre>";
}

// VULNERABILITY: passthru() with user input
if (isset($_POST['run'])) {
    echo "<h2>Running Command:</h2>";
    // VULNERABILITY: Command injection
    passthru($_POST['run']);
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Admin Debug Console</title>
</head>
<body>
    <h1>Debug Console (Admin)</h1>

    <h2>PHP Eval</h2>
    <form method="POST">
        <textarea name="code" rows="10" cols="50" placeholder="Enter PHP code to execute..."><?php echo @$_POST['code']; ?></textarea>
        <br>
        <button type="submit">Execute PHP</button>
    </form>

    <h2>Ping Tool</h2>
    <form method="POST">
        <input type="text" name="ping" placeholder="Enter hostname/IP">
        <button type="submit">Ping</button>
    </form>

    <h2>Run Command</h2>
    <form method="POST">
        <input type="text" name="run" placeholder="Enter system command">
        <button type="submit">Run</button>
    </form>

    <h2>Quick Commands</h2>
    <ul>
        <li><a href="?cmd=id">whoami</a></li>
        <li><a href="?cmd=ls -la">List files</a></li>
        <li><a href="?cmd=cat /etc/passwd">View passwd</a></li>
        <li><a href="?cmd=env">Environment</a></li>
    </ul>

    <!-- VULNERABILITY: Server information disclosure -->
    <h2>Server Info</h2>
    <pre><?php phpinfo(); ?></pre>
</body>
</html>
