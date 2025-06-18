let consultantId;
let table;

async function getConsultantId() {
  const res = await fetch("/api/consultant_id");
  const data = await res.json();
  return data.consultant_id;
}

async function getProjects() {
  const res = await fetch("/api/projects");
  const data = await res.json();
  return data.map(p => ({ label: p.name, value: p.id }));
}

async function setupGrid() {
  consultantId = await getConsultantId();
  const projectOptions = await getProjects();

  table = new Tabulator("#hours-table", {
    height: 400,
    layout: "fitColumns",
    addRowPos: "top",
    history: true,
    placeholder: "No Data Set",
    columns: [
      { title: "Date", field: "WorkDate", editor: "input" },
      { title: "Client", field: "Client", editor: "input" },
      { title: "Project", field: "Project", editor: "select", editorParams: { values: projectOptions } },
      { title: "Description", field: "WorkDescription", editor: "input" },
      { title: "Hours", field: "WorkedHours", editor: "number", bottomCalc: "sum" },
      {
        formatter: "buttonCross",
        width: 40,
        hozAlign: "center", // <-- Fix here
        cellClick: function (e, cell) {
          cell.getRow().delete();
        }
      }
    ]
  });

  // Load previously logged entries
  const now = new Date();
  await loadLoggedHours(now.getFullYear(), now.getMonth() + 1);

  document.getElementById("save-btn").addEventListener("click", saveGridData);
}

async function loadLoggedHours(year, month) {
  try {
    const response = await fetch(`/api/logged_hours?year=${year}&month=${month}`);
    const result = await response.json();

    if (!response.ok || !result.data) {
      console.error("Failed to load logged hours:", result.error);
      return;
    }

    table.setData(result.data);
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