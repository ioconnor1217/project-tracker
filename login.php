<?php
// login.php
require_once 'db.php';
require_once 'validation.php';
$pageTitle = 'Login';
require 'header.php';  // header will not render nav for guests

$msg = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Replace null-coalesce with isset()
    $username = isset($_POST['username']) ? $_POST['username'] : '';
    $password = isset($_POST['password']) ? $_POST['password'] : '';

    // validate before querying
    if (!is_valid_username($username)) {
        $msg = "Username contains invalid characters.";
    } elseif (!is_valid_password($password)) {
        $msg = "Password must be at least 8 chars, one upper, one lower, one digit, one special.";
    } else {
        $user = search_username($username);
        if ($user && $password === trim($user['Password'])) {
            $_SESSION['user'] = $user['UserName'];
            header('Location: dashboard.php');
            exit;
        } else {
            $msg = "Invalid username or password.";
        }
    }
}
?>

<h2>Login</h2>
<?php if ($msg): ?>
  <p class="error"><?php echo htmlspecialchars($msg); ?></p>
<?php endif; ?>

<form method="post" class="login-form">
  <label>Username</label>
  <input name="username" required>
  <label>Password</label>
  <input type="password" name="password" required>
  <button type="submit">Login</button>
</form>

<?php require 'footer.php'; ?>