let consultantId;
let table;
let selectedDate = new Date();
let clientOptions = [];
let projectOptions = [];

async function getConsultantId() {
  const res = await fetch("/api/consultant_id");
  const data = await res.json();
  return data.consultant_id;
}

async function getClients() {
  const res = await fetch("/api/clients");
  const data = await res.json();
  return data.map(c => ({ label: c.name, value: c.name }));
}

async function getProjects() {
  const res = await fetch("/api/projects");
  const data = await res.json();
  return data.map(p => ({ label: p.name, value: p.name }));
}

async function setupGrid() {
  consultantId = await getConsultantId();
  clientOptions = await getClients();
  projectOptions = await getProjects();

  table = new Tabulator("#hours-table", {
    height: 400,
    layout: "fitColumns",
    addRowPos: "top",
    history: true,
    placeholder: "No Data Set",
    columns: [
      { title: "Date", field: "date", editor: "input" },
      { title: "Client", field: "client", editor: "select", editorParams: { values: clientOptions } },
      { title: "Project", field: "project", editor: "select", editorParams: { values: projectOptions } },
      { title: "Description", field: "description", editor: "input" },
      { title: "Hours", field: "hours", editor: "number", bottomCalc: "sum" },
      {
        formatter: "buttonCross",
        width: 40,
        hozAlign: "center",
        cellClick: function (e, cell) {
          cell.getRow().delete();
        }
      }
    ]
  });

  setupDateControls();
  reloadGridForSelectedDate();
  document.getElementById("save-btn").addEventListener("click", saveGridData);
}

function reloadGridForSelectedDate() {
  const year = selectedDate.getFullYear();
  const month = selectedDate.getMonth() + 1;
  loadLoggedHours(year, month);
}

function setupDateControls() {
  const datePicker = document.getElementById("date-picker");
  const prevBtn = document.getElementById("prev-day");
  const nextBtn = document.getElementById("next-day");

  datePicker.value = selectedDate.toISOString().split('T')[0];

  datePicker.addEventListener("change", (e) => {
    selectedDate = new Date(e.target.value);
    reloadGridForSelectedDate();
  });

  prevBtn.addEventListener("click", () => {
    selectedDate.setMonth(selectedDate.getMonth() - 1);
    datePicker.value = selectedDate.toISOString().split('T')[0];
    reloadGridForSelectedDate();
  });

  nextBtn.addEventListener("click", () => {
    selectedDate.setMonth(selectedDate.getMonth() + 1);
    datePicker.value = selectedDate.toISOString().split('T')[0];
    reloadGridForSelectedDate();
  });
}

async function loadLoggedHours(year, month) {
  try {
    const response = await fetch(`/api/logged_hours?year=${year}&month=${month}`);
    const result = await response.json();

    let mapped = [];
    if (response.ok && result.data && result.data.length) {
      mapped = result.data.map(row => ({
        date: row.date || row.WorkDate,
        client: row.client || row.Client,
        project: row.project || row.Project,
        description: row.description || row.WorkDescription,
        hours: row.hours || row.WorkedHours
      }));
    } else {
      // No data: add a blank row with placeholders
      mapped = [{
        date: "Add New Date...",
        client: "Select Client...",
        project: "Select Project...",
        description: "Add Description...",
        hours: "Add Hours..."
      }];
    }
    table.setData(mapped);
  } catch (err) {
    console.error("Fetch error loading logged hours:", err);
    alert("Could not load logged hours.");
  }
}

async function saveGridData() {
  const data = table.getData();

  if (!data.length) {
    alert("No rows to save.");
    return;
  }

  try {
    const response = await fetch("/submit_hours", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ consultant_id: consultantId, entries: data })
    });

    const result = await response.json();
    alert(result.message || "Saved.");
  } catch (err) {
    console.error("Save failed:", err);
    alert("Something went wrong while saving.");
  }
}

// Kick off grid setup on page load
window.addEventListener("DOMContentLoaded", () => {
  const currentPath = window.location.pathname;
  if (currentPath === "/log_hours") {
    setupGrid();
  }
});