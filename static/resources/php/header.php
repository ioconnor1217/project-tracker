<?php
// header.php

// Start session if none exists
if (session_id() === '') {
    session_start();
}

// enforce a 5-minute timeout
require_once 'validation.php';
enforce_session_timeout(300);
?>
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title><?php echo htmlspecialchars(isset($pageTitle) ? $pageTitle : 'ProjectTracker'); ?></title>
  <link rel="stylesheet" href="assets/style.css">
</head>
<body>

<!-- Only show the sidebar and navigation if the user is logged in -->
<?php if (isset($_SESSION['user'])): ?>
  <div class="sidebar">
    <nav>
      <ul>
        <li><a href="dashboard.php">Dashboard</a></li>
        <li><a href="hours.php">Log Hours</a></li>
        <li><a href="logout.php">Logout</a></li>
      </ul>
    </nav>
  </div>
<?php endif; ?>

<main>