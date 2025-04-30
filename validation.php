<?php
function is_valid_username($username) {
    // Only letters, numbers, spaces, apostrophes, periods, and hyphens
    return preg_match("/^[a-zA-Z\d\s.'-]+$/", $username);
}

function is_valid_email($email) {
    return filter_var($email, FILTER_VALIDATE_EMAIL);
}

function is_valid_password($password) {
    return true;

    // $pattern = '/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/';
    // return preg_match($pattern, $password);
}

/**
 * @param int $timeout Number of seconds of allowed inactivity.
 */
function enforce_session_timeout($timeout = 300) {
    // Start session if none exists
    if (session_id() === '') {
        session_start();
    }

    // Check last activity
    if (isset($_SESSION['last_activity'])) {
        $inactive = time() - $_SESSION['last_activity'];
        if ($inactive > $timeout) {
            // Session has expired
            session_unset();
            session_destroy();
            header('Location: login.php?timeout=1');
            exit;
        }
    }

    // Update last activity timestamp
    $_SESSION['last_activity'] = time();
}