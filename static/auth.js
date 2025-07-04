// Constants
const TIMEOUT_MS = 300000;
let timeout; // For session timeout enforcement

// DOM Elements
const loginForm = document.getElementById("login-form");
const logoutLink = document.getElementById("logout");
const msgBox = document.getElementById("msg");
const usernameSpan = document.getElementById("username");

// Validate username
function validateUsername(username) {
  const usernamePattern = /^[a-zA-Z0-9_]{3,20}$/;
  return usernamePattern.test(username);
}

// Optional password validation
/*
function validatePassword(password) {
  const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/;
  return passwordPattern.test(password);
}
*/

// Enforce session timeout
function enforceSession() {
  const lastActivity = parseInt(sessionStorage.getItem("lastActivity"), 10);
  const now = Date.now();
  if (isNaN(lastActivity) || now - lastActivity > TIMEOUT_MS) {
    alert("Session expired. Please log in again.");
    logoutUser();
  } else {
    sessionStorage.setItem("lastActivity", now);
  }
}

// Login user
function loginUser(username) {
  sessionStorage.setItem("user", username);
  sessionStorage.setItem("lastActivity", Date.now());
  window.location.href = "/dashboard";
}

// Logout user
function logoutUser(e) {
  if (e) e.preventDefault();
  sessionStorage.removeItem("user");
  sessionStorage.removeItem("lastActivity");
  window.location.href = "/";
}

// Handle login form submission
function submitLogin(e) {
  e.preventDefault();
  const username = loginForm.username.value.trim();
  const password = loginForm.password.value.trim();

  if (!username || !password) {
    alert("Please enter both username and password.");
    return;
  }

  if (!validateUsername(username)) {
    if (msgBox) msgBox.textContent = "Invalid username.";
    return;
  }

  fetch("/api/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.success) {
        loginUser(username);
      } else {
        alert(data.errorMessage || "Login failed.");
      }
    })
    .catch(() => {
      alert("Something went wrong. Please try again later.");
    });
}

// Init page
function initPage() {
  const user = sessionStorage.getItem("user");
  const currentPath = window.location.pathname;

  if (!user && currentPath !== "/" && currentPath !== "/login") {
    window.location.href = "/";
  } else if (user) {
    if (usernameSpan) usernameSpan.textContent = user;
    if (logoutLink) logoutLink.addEventListener("click", logoutUser);
    enforceSession();
    timeout = setInterval(enforceSession, 60000);

    if (currentPath === "/log_hours") {
      populateDropdowns();
      initDateControls();
    } else if (currentPath === "/view_hours") {
      initMonthControls();
    }
  }
}

// Submit hours
async function submitHours() {
  const table = document.querySelector("#hours-table tbody");
  const rows = Array.from(table.rows);
  const data = [];
  const date = formatDate(currentDate); // use central date picker value

  rows.forEach((row) => {
    const project_id = row.querySelector(".project-select").value;
    const description = row.querySelector(".desc-input").value.trim();
    const hours = parseFloat(row.querySelector(".hours-input").value);
  
    if (!project_id || !description || isNaN(hours)) return;
  
    data.push({
      project_id: parseInt(project_id),
      date,
      description,
      hours
    });
  });

  if (!data.length) {
    alert("Please fill in at least one complete row before submitting.");
    return;
  }

  // Fetch consultant ID dynamically from Flask endpoint
  let consultantId;
  try {
    const response = await fetch("/api/consultant_id");
    if (!response.ok) throw new Error("Failed to retrieve consultant ID");
    const result = await response.json();
    consultantId = result.consultant_id;
  } catch (error) {
    console.error("Could not get consultant ID:", error);
    alert("Error retrieving consultant ID. Please log in again.");
    return;
  }

  const payload = {
    consultant_id: consultantId,
    entries: data
  };

  console.log("Sending payload:", payload);

  try {
    const response = await fetch(`/submit_hours`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const result = await response.json();
    if (result.status === "success") {
      alert("Hours submitted successfully!");
    } else {
      console.error("Submission failed:", result.message, result.trace || "");
      alert(`Submission failed: ${result.message}`);
    }
  } catch (err) {
    console.error("Fetch error:", err);
    alert("Something went wrong. Please try again later.");
  }
}

// Populate project dropdowns only
async function populateDropdowns() {
  const projectsRes = await fetch("/api/projects");
  const projects = await projectsRes.json();

  // Debug output to console
  console.log("Projects fetched for dropdown:", projects);

  const projectOptions = projects.map(p => `<option value="${p.id}">${p.name}</option>`).join("");

  document.querySelectorAll(".project-select").forEach(select => {
    select.innerHTML = `<option value="">-- Select Project --</option>` + projectOptions;
  });
}

// Remove project/client creation listeners
window.addEventListener("DOMContentLoaded", () => {
  initPage();
  if (loginForm) {
    loginForm.addEventListener("submit", submitLogin);
  }
});

// --- Date Handling Variables ---
let currentDate = new Date();

function formatDate(date) {
  return date.toISOString().split('T')[0];
}

function updateDateUI() {
  const picker = document.getElementById("date-picker");
  const formatted = formatDate(currentDate);

  if (picker) picker.value = formatted;
}

function initDateControls() {
  document.getElementById("prev-day").addEventListener("click", () => {
    currentDate.setDate(currentDate.getDate() - 1);
    updateDateUI();
  });

  document.getElementById("next-day").addEventListener("click", () => {
    currentDate.setDate(currentDate.getDate() + 1);
    updateDateUI();
  });

  document.getElementById("date-picker").addEventListener("change", (e) => {
    currentDate = new Date(e.target.value);
    updateDateUI();
  });

  updateDateUI(); // Initialize on load
}

// --- Month Navigation & Display ---

let currentYear = new Date().getFullYear();
let currentMonth = new Date().getMonth(); // 0-indexed

function formatMonthYear(year, month) {
  const monthNames = ["January", "February", "March", "April", "May", "June",
                      "July", "August", "September", "October", "November", "December"];
  return `${monthNames[month]} ${year}`;
}

function updateMonthUI() {
  const display = document.getElementById("month-display");
  if (display) {
    display.textContent = formatMonthYear(currentYear, currentMonth);
  }
  fetchLoggedHours(currentYear, currentMonth + 1); // backend expects 1-indexed month
}

function changeMonth(offset) {
  currentMonth += offset;
  if (currentMonth < 0) {
    currentMonth = 11;
    currentYear -= 1;
  } else if (currentMonth > 11) {
    currentMonth = 0;
    currentYear += 1;
  }
  updateMonthUI();
}

function initMonthControls() {
  document.getElementById("prev-month").addEventListener("click", () => changeMonth(-1));
  document.getElementById("next-month").addEventListener("click", () => changeMonth(1));
  updateMonthUI(); // Initial load
}

async function fetchLoggedHours(year, month) {
  try {
    const response = await fetch(`/api/logged_hours?year=${year}&month=${month}`);
    const result = await response.json();

    if (!response.ok || !result.data) {
      throw new Error(result.error || "Failed to load logged hours.");
    }

    populateLoggedHoursTable(result.data);
  } catch (err) {
    console.error("Fetch error:", err);
    // alert("Could not load logged hours."); // Disabled to prevent popup in View Hours
  }
}

function populateLoggedHoursTable(data) {
  const tbody = document.querySelector("#logged-hours-table tbody");
  tbody.innerHTML = "";

  if (!data.length) {
    const row = document.createElement("tr");
    const cell = document.createElement("td");
    cell.colSpan = 5;
    cell.textContent = "No hours logged for this month.";
    row.appendChild(cell);
    tbody.appendChild(row);
    return;
  }

  data.forEach(entry => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${entry.Client}</td>
      <td>${entry.Project}</td>
      <td>${entry.WorkDate}</td>
      <td>${entry.WorkDescription}</td>
      <td>${entry.WorkedHours}</td>
    `;
    tbody.appendChild(row);
  });
}