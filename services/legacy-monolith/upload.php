<?php
/**
 * File Upload Handler
 * WARNING: INTENTIONALLY VULNERABLE
 *
 * VULNERABILITIES:
 * - Unrestricted file upload
 * - No file type validation
 * - Path traversal
 * - Remote code execution via uploaded files
 */

require_once 'config.php';
require_once 'includes/functions.php';

session_start();

$message = '';
$uploaded_file = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_FILES['file'])) {
        $file = $_FILES['file'];

        // VULNERABILITY: Using user-provided filename directly
        $filename = $_POST['filename'] ?? $file['name'];

        // VULNERABILITY: Path traversal possible
        // Attack: filename=../../../var/www/html/shell.php
        $upload_path = UPLOAD_DIR . $filename;

        // VULNERABILITY: No file extension validation
        // Can upload .php files for RCE

        // VULNERABILITY: No MIME type validation
        // Content-Type header can be spoofed

        // VULNERABILITY: No file content validation
        // Malicious files can be uploaded

        if (move_uploaded_file($file['tmp_name'], $upload_path)) {
            $message = "File uploaded successfully: " . $filename;
            $uploaded_file = $upload_path;

            // VULNERABILITY: SQL Injection when logging upload
            $user_id = isset($_SESSION['user_id']) ? $_SESSION['user_id'] : 0;
            $query = "INSERT INTO uploads (filename, user_id, path) VALUES ('$filename', $user_id, '$upload_path')";
            mysqli_query($GLOBALS['db'], $query);
        } else {
            // VULNERABILITY: Error message reveals server paths
            $message = "Upload failed. Error: " . error_get_last()['message'];
        }
    }
}

// VULNERABILITY: File download with path traversal
if (isset($_GET['download'])) {
    $file_to_download = $_GET['download'];
    // VULNERABILITY: Arbitrary file read
    $file_path = UPLOAD_DIR . $file_to_download;

    if (file_exists($file_path)) {
        header('Content-Type: application/octet-stream');
        header('Content-Disposition: attachment; filename="' . basename($file_path) . '"');
        // VULNERABILITY: Reading arbitrary files
        readfile($file_path);
        exit;
    }
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>File Upload</title>
</head>
<body>
    <h1>Upload File</h1>

    <?php if ($message): ?>
        <!-- VULNERABILITY: XSS in message -->
        <div class="message"><?php echo $message; ?></div>
    <?php endif; ?>

    <form method="POST" enctype="multipart/form-data">
        <!-- VULNERABILITY: No CSRF token -->
        <label>Select File:</label>
        <input type="file" name="file">

        <label>Custom Filename (optional):</label>
        <input type="text" name="filename" placeholder="custom_name.ext">

        <button type="submit">Upload</button>
    </form>

    <h2>Uploaded Files</h2>
    <?php
    // VULNERABILITY: Directory listing
    $files = scandir(UPLOAD_DIR);
    foreach ($files as $f) {
        if ($f != '.' && $f != '..') {
            // VULNERABILITY: XSS in filename display
            echo "<a href='?download=$f'>$f</a><br>";
        }
    }
    ?>

    <!-- VULNERABILITY: Debug info -->
    <?php if (isset($_GET['debug'])): ?>
        <pre>Upload Directory: <?php echo UPLOAD_DIR; ?></pre>
        <pre>$_FILES: <?php print_r($_FILES); ?></pre>
    <?php endif; ?>
</body>
</html>
