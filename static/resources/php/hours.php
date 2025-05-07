<?php
// hours.php
$pageTitle = 'Log Hours';
require 'header.php';

if (!isset($_SESSION['user'])) {
    header('Location: login.php');
    exit;
}
?>

<h2>Log Hours Here</h2>

<?php require 'footer.php'; ?>