let consultantId;
let table;
let selectedDate = new Date();
let projectOptions = [];

// Set selectedDate to the user's local date (not UTC)
let now = new Date();
selectedDate = new Date(now.getFullYear(), now.getMonth(), now.getDate());

async function getConsultantId() {
  const res = await fetch("/api/consultant_id");
  const data = await res.json();
  return data.consultant_id;
}

async function getProjects() {
  const res = await fetch("/api/projects");
  const data = await res.json();
  // Use id for value, name for label
  return data.map(p => ({ label: p.name, value: p.id }));
}

async function setupGrid() {
  consultantId = await getConsultantId();
  projectOptions = await getProjects();

  table = new Tabulator("#hours-table", {
    layout: "fitColumns",
    addRowPos: "top",
    history: true,
    placeholder: "No Data Set",
    columns: [
      {
        title: "Project",
        field: "project",
        editor: "select",
        editorParams: function() {
          return {
            values: projectOptions,
            clearable: true,
            placeholder: "Choose a project"
          };
        },
        formatter: function(cell) {
          const value = cell.getValue();
          if (value === null || value === undefined || value === "") {
            return '<span style="color:#888">Choose a project</span>';
          }
          const found = projectOptions.find(opt => opt.value === value);
          return found ? found.label : value;
        }
      },
      {
        title: "Description",
        field: "description",
        editor: "input",
        formatter: function(cell) {
          const value = cell.getValue();
          if (!value || value === "Enter description...") {
            return '<span style="color:#888">Enter description...</span>';
          }
          return value;
        }
      },
      {
        title: "Hours",
        field: "hours",
        editor: "number",
        formatter: function(cell) {
          const value = cell.getValue();
          if (!value || value === 0 || value === "0" || value === "") {
            return '<span style="color:#888">0</span>';
          }
          return value;
        },
        bottomCalc: "sum",
        bottomCalcFormatter: function(cell) { return "Total Daily Hours: " + cell.getValue(); }
      },
      {
        formatter: "buttonCross",
        width: 40,
        hozAlign: "center",
        cellClick: function (e, cell) {
          cell.getRow().delete();
        }
      }
    ],
    cellEditing: function(cell) {
      // Clear placeholder for description and hours on edit
      if (cell.getField() === "description" && (cell.getValue() === "Enter description..." || !cell.getValue())) {
        cell.setValue("");
      }
      if (cell.getField() === "hours" && (!cell.getValue() || cell.getValue() === 0 || cell.getValue() === "0")) {
        cell.setValue("");
      }
    },
    cellEdited: function(cell) {
      // Restore placeholder if left empty
      if (cell.getField() === "description" && (!cell.getValue() || cell.getValue().trim() === "")) {
        cell.setValue("Enter description...");
      }
      if (cell.getField() === "hours" && (!cell.getValue() || cell.getValue() === "")) {
        cell.setValue(0);
      }
    }
  });

  setupDateControls();
  reloadGridForSelectedDate();
  document.getElementById("save-btn").addEventListener("click", saveGridData);
}

function reloadGridForSelectedDate() {
  const year = selectedDate.getFullYear();
  const month = selectedDate.getMonth() + 1;
  const day = selectedDate.getDate();
  loadLoggedHours(year, month, day);
}

function setupDateControls() {
  const datePicker = document.getElementById("date-picker");
  const prevBtn = document.getElementById("prev-day");
  const nextBtn = document.getElementById("next-day");

  datePicker.value = selectedDate.toISOString().split('T')[0];

  datePicker.addEventListener("change", (e) => {
    // Parse as local date to avoid timezone issues
    const [year, month, day] = e.target.value.split('-').map(Number);
    selectedDate = new Date(year, month - 1, day);
    reloadGridForSelectedDate();
  });

  prevBtn.addEventListener("click", () => {
    selectedDate.setDate(selectedDate.getDate() - 1);
    datePicker.value = selectedDate.toISOString().split('T')[0];
    reloadGridForSelectedDate();
  });

  nextBtn.addEventListener("click", () => {
    selectedDate.setDate(selectedDate.getDate() + 1);
    datePicker.value = selectedDate.toISOString().split('T')[0];
    reloadGridForSelectedDate();
  });
}

async function loadLoggedHours(year, month, day) {
  console.log('[DEBUG] Loading logged hours for:', { year, month, day });
  try {
    const response = await fetch(`/api/logged_hours?year=${year}&month=${month}&day=${day}`);
    const result = await response.json();

    let mapped = [];
    if (response.ok && result.data && result.data.length) {
      mapped = result.data.map(row => {
        // Map project to id for logged entries
        let project_id = null;
        if (typeof row.project === 'number') {
          project_id = row.project;
        } else if (row.project_id) {
          project_id = row.project_id;
        } else if (typeof row.project === 'string') {
          // Try to map from label to id if needed
          const found = projectOptions.find(opt => opt.label === row.project);
          if (found) project_id = found.value;
        }
        return {
          project: project_id,
          description: row.description || row.WorkDescription || "",
          hours: row.hours || row.WorkedHours || 0.0
        };
      });
    }
    // Always append a blank placeholder row for new entry
    mapped.push({
      project: null, // null so Tabulator select shows placeholder
      description: "Enter description...",
      hours: 0.0
    });
    table.setData(mapped);
  } catch (err) {
    console.error("Fetch error loading logged hours:", err);
    alert("Could not load logged hours.");
  }
}

async function saveGridData() {
  const data = table.getData();

  // Exclude the last row if it's the placeholder (no project, no description, hours 0.0)
  const filteredData = data.filter(row => row.project !== null || (row.description && row.description !== "Enter description...") || (row.hours && Number(row.hours) !== 0));

  // Map project (id or label) to project_id and include the selected date
  const entries = filteredData.map(row => {
    let project_id = null;
    if (typeof row.project === "number") {
      project_id = row.project;
    } else if (typeof row.project === "string") {
      const projectObj = projectOptions.find(opt => opt.label === row.project);
      if (projectObj) project_id = projectObj.value;
    }
    return {
      project_id,
      description: row.description && row.description.trim() && row.description !== "Enter description..." ? row.description.trim() : null,
      hours: row.hours && !isNaN(Number(row.hours)) ? Number(row.hours) : null,
      date: selectedDate.toISOString().split('T')[0]
    };
  });

  // Filter out rows with missing required fields
  const validEntries = entries.filter(e => e.project_id && e.description && e.hours !== null && e.hours !== "");

  if (!validEntries.length) {
    // Find the first invalid row for a more specific error
    const firstInvalid = entries.find(e => !e.project_id || !e.description || e.hours === null || e.hours === "");
    let msg = "Please select a project, enter a description, and enter hours before saving.";
    if (firstInvalid) {
      if (!firstInvalid.project_id) msg = "Please choose a project.";
      else if (!firstInvalid.description) msg = "Please enter a description.";
      else if (firstInvalid.hours === null || firstInvalid.hours === "") msg = "Please enter a valid number of hours.";
    }
    alert(msg);
    return;
  }

  try {
    const response = await fetch("/submit_hours", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ consultant_id: consultantId, entries: validEntries })
    });

    const result = await response.json();
    alert(result.message || "Saved.");

    // After successful save, reload grid and add a new placeholder row
    await reloadGridForSelectedDate();
    // After reload, a new placeholder row will be appended automatically
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