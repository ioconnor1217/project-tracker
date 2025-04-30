<?php
$pageTitle = 'Dashboard';
require 'header.php';

if (!isset($_SESSION['user'])) {
  header('Location: login.php');
  exit;
}
?>

<h2 class="welcome">Welcome, <?= htmlspecialchars($_SESSION['user']) ?>!</h2>
<p>Use the sidebar to make a selection</p>

<?php require 'footer.php'; ?>