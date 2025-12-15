<?php
/**
 * Simple Router
 * WARNING: INTENTIONALLY VULNERABLE - LFI/RFI
 */

// VULNERABILITY: Remote File Inclusion possible if allow_url_include is ON
function route($page) {
    // VULNERABILITY: Local File Inclusion
    // Attack: page=../../../etc/passwd%00
    // Attack: page=php://filter/convert.base64-encode/resource=config
    $allowed_pages = array('home', 'about', 'contact', 'products');

    if (in_array($page, $allowed_pages)) {
        include("pages/" . $page . ".php");
    } else {
        // VULNERABILITY: Still includes user input
        // The validation above is flawed - path traversal still possible
        include("pages/" . $page . ".php");
    }
}

// VULNERABILITY: Another LFI vector
function load_template($template) {
    $template_path = $_GET['template_dir'] ?? 'templates';
    // VULNERABILITY: Both directory and file are user-controlled
    include($template_path . '/' . $template . '.php');
}

// VULNERABILITY: Include via parameter
function include_module() {
    if (isset($_GET['module'])) {
        // VULNERABILITY: Direct include of user input
        include($_GET['module']);
    }
}

// VULNERABILITY: Log Poisoning setup
function log_request() {
    $log_file = '/var/log/access.log';
    $user_agent = $_SERVER['HTTP_USER_AGENT'];
    // VULNERABILITY: User-Agent written to log (log poisoning)
    file_put_contents($log_file, $user_agent . "\n", FILE_APPEND);
}
