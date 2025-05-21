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
  if (e) e.preventDefault();
  sessionStorage.removeItem('user');
  sessionStorage.removeItem('lastActivity');
  window.location.href = '/';
}

async function submitHours() {
  const table = document.getElementById('hours-table').getElementsByTagName('tbody')[0];
  const rows = Array.from(table.rows);
  const data = [];

  for (const row of rows) {
    const project_id = row.querySelector('.project-select').value;
    const client_id = row.querySelector('.client-select').value;
    const date = row.querySelector('.date-input').value;
    const description = row.querySelector('.desc-input').value.trim();
    const hours = parseFloat(row.querySelector('.hours-input').value);

    if (!project_id || !client_id || !date || !description || isNaN(hours)) continue;

    data.push({
      project_id: parseInt(project_id),
      client_id: parseInt(client_id),
      date,
      description,
      hours
    });
  }

  if (data.length === 0) {
    alert('Please fill in at least one complete row before submitting.');
    return;
  }

  try {
    const response = await fetch('/submit_hours', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });

    const result = await response.json();
    if (result.status === 'success') {
      alert('Hours submitted successfully!');
    } else {
      alert('Submission failed.');
    }
  } catch (error) {
    console.error('Error submitting hours:', error);
    alert('An error occurred while submitting hours.');
  }
}

async function populateDropdowns() {
  const projectSelects = document.querySelectorAll('.project-select');
  const clientSelects = document.querySelectorAll('.client-select');

  const [projectsRes, clientsRes] = await Promise.all([
    fetch('/api/projects'),
    fetch('/api/clients')
  ]);

  const projects = await projectsRes.json();
  const clients = await clientsRes.json();

  const projectOptions = projects.map(p => `<option value="${p.id}">${p.name}</option>`).join('');
  const clientOptions = clients.map(c => `<option value="${c.id}">${c.name}</option>`).join('');

  projectSelects.forEach(select => {
    select.innerHTML = `
      <option value="">-- Select or Add Project --</option>
      ${projectOptions}
      <option value="__new__">+ Add New Project</option>
    `;
  });

  clientSelects.forEach(select => {
    select.innerHTML = `
      <option value="">-- Select or Add Client --</option>
      ${clientOptions}
      <option value="__new__">+ Add New Client</option>
    `;
  });
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

    // ✅ Moved inside initPage to ensure DOM is ready
    if (currentPath === '/hours') {
      populateDropdowns();
    }
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

  if (!validateUsername(username)) {
    msgBox.textContent = 'Invalid username.';
  } else {
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

// ✅ DOM is fully ready before initPage is called
window.addEventListener('DOMContentLoaded', initPage);

document.addEventListener('change', async (e) => {
  if (e.target.classList.contains('project-select') && e.target.value === '__new__') {
    const newProject = prompt("Enter new project name:");
    if (!newProject) return;

    const exists = await checkDuplicate('/api/check_project', newProject);
    if (exists) return alert("Project already exists.");

    const id = await createNewItem('/api/create_project', newProject);
    if (id) {
      await populateDropdowns();
      e.target.value = id;
    }
  }

  if (e.target.classList.contains('client-select') && e.target.value === '__new__') {
    const newClient = prompt("Enter new client name:");
    if (!newClient) return;

    const exists = await checkDuplicate('/api/check_client', newClient);
    if (exists) return alert("Client already exists.");

    const id = await createNewItem('/api/create_client', newClient);
    if (id) {
      await populateDropdowns();
      e.target.value = id;
    }
  }
});

async function checkDuplicate(url, name) {
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name })
  });
  const result = await res.json();
  return result.exists;
}

async function createNewItem(url, name) {
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name })
  });
  const result = await res.json();
  return result.id;
}

// Attach login event if login form exists
if (loginForm) {
  loginForm.addEventListener('submit', submitLogin);
}