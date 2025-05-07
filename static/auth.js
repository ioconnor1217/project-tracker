const loginForm = document.getElementById('login-form');
const logoutLink = document.getElementById('logout');
const msgBox = document.getElementById('msg');
const usernameSpan = document.getElementById('username');

// Simulate session timeout (5 minutes = 300000 ms)
const TIMEOUT_MS = 300000;
let timeout;

function loginUser(username) {
  sessionStorage.setItem('user', username);
  sessionStorage.setItem('lastActivity', Date.now());
  window.location.href = '/dashboard';
}

function logoutUser(e) {
  if (e) e.preventDefault(); // prevent default link behavior
  sessionStorage.removeItem('user');
  sessionStorage.removeItem('lastActivity');
  window.location.href = '/';
}

function enforceSession() {
  const lastActivity = parseInt(sessionStorage.getItem('lastActivity'), 10);
  const now = Date.now();
  if (isNaN(lastActivity) || now - lastActivity > TIMEOUT_MS) {
    alert('Session expired. Please log in again.');
    logoutUser();
  } else {
    sessionStorage.setItem('lastActivity', now);
  }
}

function initPage() {
  const user = sessionStorage.getItem('user');
  const currentPath = window.location.pathname;

  if (!user && currentPath !== '/' && currentPath !== '/login') {
    window.location.href = '/';
  } else if (user) {
    if (usernameSpan) usernameSpan.textContent = user;
    if (logoutLink) logoutLink.addEventListener('click', logoutUser);
    enforceSession();
    timeout = setInterval(enforceSession, 60000);
  }
}

function validateUsername(username) {
  const usernamePattern = /^[a-zA-Z0-9_]{3,20}$/;
  return usernamePattern.test(username);
}

// Temporarily commented out password validation
/*
function validatePassword(password) {
  const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/;
  return passwordPattern.test(password);
}
*/

function submitLogin(e) {
  e.preventDefault();
  const username = loginForm.username.value.trim();
  const password = loginForm.password.value.trim();

  if (!username && !password) {
    alert("Please enter both username and password.");
    return;
  }
  if (!username) {
    alert("Please enter your username.");
    return;
  }
  if (!password) {
    alert("Please enter your password.");
    return;
  }

  // Validate username and password (password validation commented out for now)
  if (!validateUsername(username)) {
    msgBox.textContent = 'Invalid username.';
  } 
  // Temporarily bypassing password validation
  /*
  else if (!validatePassword(password)) {
    msgBox.textContent = 'Password must be at least 8 chars, one upper, one lower, one digit, one special.';
  }
  */
  else {
    // Send login data to the server for further validation
    fetch('/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        sessionStorage.setItem('user', username);
        sessionStorage.setItem('lastActivity', Date.now());
        window.location.href = '/dashboard';
      } else {
        alert(data.errorMessage);
      }
    })
    .catch(() => {
      alert("Something went wrong. Please try again later.");
    });
  }
}

// --- Initialize page (protect routes) ---
window.addEventListener('DOMContentLoaded', initPage);

// Handle form submission
if (loginForm) {
  loginForm.addEventListener('submit', submitLogin);
}