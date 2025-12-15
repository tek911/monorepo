<?php
/**
 * User Management Page
 * WARNING: INTENTIONALLY VULNERABLE
 *
 * VULNERABILITIES:
 * - SQL Injection
 * - IDOR (Insecure Direct Object Reference)
 * - Missing authorization
 * - Mass assignment
 */

require_once 'config.php';
require_once 'includes/functions.php';

session_start();

// VULNERABILITY: No authentication check
// Anyone can access user data

$action = isset($_GET['action']) ? $_GET['action'] : 'list';
$user_id = isset($_GET['id']) ? $_GET['id'] : '';

switch ($action) {
    case 'view':
        // VULNERABILITY: IDOR - no authorization check
        // VULNERABILITY: SQL Injection
        $query = "SELECT * FROM users WHERE id = $user_id";
        $result = mysqli_query($GLOBALS['db'], $query);
        $user = mysqli_fetch_assoc($result);

        // VULNERABILITY: Exposing sensitive data (password hash, SSN, etc.)
        echo "<pre>";
        print_r($user);
        echo "</pre>";
        break;

    case 'delete':
        // VULNERABILITY: No CSRF protection
        // VULNERABILITY: SQL Injection
        // VULNERABILITY: No authorization
        $query = "DELETE FROM users WHERE id = $user_id";
        mysqli_query($GLOBALS['db'], $query);
        header("Location: users.php?message=User deleted");
        break;

    case 'update':
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            // VULNERABILITY: Mass assignment - all POST data used
            $fields = array();
            foreach ($_POST as $key => $value) {
                // VULNERABILITY: SQL Injection
                $fields[] = "$key = '$value'";
            }
            $update_query = "UPDATE users SET " . implode(', ', $fields) . " WHERE id = $user_id";
            mysqli_query($GLOBALS['db'], $update_query);

            // VULNERABILITY: Role escalation possible via mass assignment
            // POST: role=admin
        }
        break;

    case 'list':
    default:
        // VULNERABILITY: SQL Injection in order parameter
        $order = isset($_GET['order']) ? $_GET['order'] : 'id';
        $query = "SELECT * FROM users ORDER BY $order";
        $result = mysqli_query($GLOBALS['db'], $query);

        echo "<h1>Users</h1>";
        echo "<table><tr><th>ID</th><th>Username</th><th>Email</th><th>Actions</th></tr>";

        while ($row = mysqli_fetch_assoc($result)) {
            echo "<tr>";
            // VULNERABILITY: Stored XSS
            echo "<td>{$row['id']}</td>";
            echo "<td>{$row['username']}</td>";
            echo "<td>{$row['email']}</td>";
            echo "<td>
                    <a href='?action=view&id={$row['id']}'>View</a>
                    <a href='?action=delete&id={$row['id']}'>Delete</a>
                  </td>";
            echo "</tr>";
        }
        echo "</table>";
        break;
}
?>
