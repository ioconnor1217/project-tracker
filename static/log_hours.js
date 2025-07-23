let consultantId;
let table;
let selectedDate = new Date();
let projectOptions = [];
let deletedRows = [];

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
    layout: "fitDataTable",
    addRowPos: "bottom",
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
          if (!value) {
            return '<span style="color:#888">Enter description...</span>';
          }
          return value;
        }
      },
      {
        title: "Hours",
        field: "hours",
        editor: "number",
        editorParams: { min: 0.01, step: 0.01 },
        resizable: true,
        formatter: function(cell) {
          const value = cell.getValue();
          if (!value || value === 0 || value === "0" || value === "") {
            return '<span style="color:#888">0</span>';
          }
          return value;
        }
      },
      {
        formatter: function(cell) {
          return '<span class="delete-x" style="color:red;cursor:pointer;font-size:1.2em;display:inline-block;width:100%;text-align:center;overflow:visible;">&#10006;</span>';
        },
        width: 60,
        hozAlign: "center",
        cellClick: function (e, cell) {
          const rowData = cell.getRow().getData();
          const hasProject = rowData.project !== null && rowData.project !== undefined && rowData.project !== "";
          const hasDescription = rowData.description && rowData.description !== "Enter description..." && rowData.description.trim() !== "";
          const hasHours = rowData.hours && !isNaN(Number(rowData.hours)) && Number(rowData.hours) > 0;
          const allRows = cell.getTable().getData();
          const isEntryRow = cell.getRow().getPosition(true) === allRows.length - 1;
          // Only allow delete if not the entry row and not the only row left
          if (hasProject && hasDescription && hasHours && !isEntryRow && allRows.length > 1) {
            deletedRows.push({
              project_id: typeof rowData.project === "number" ? rowData.project : (projectOptions.find(opt => opt.label === rowData.project)?.value),
              date: selectedDate.toISOString().split('T')[0]
            });
            cell.getRow().delete();
            // After delete, if no entry row exists at the bottom, add one
            setTimeout(() => {
              const rows = cell.getTable().getData();
              const lastRow = rows[rows.length - 1];
              const isLastEntryRow = lastRow && (!lastRow.project && (!lastRow.description || lastRow.description.trim() === "") && (!lastRow.hours || Number(lastRow.hours) === 0));
              if (!isLastEntryRow) {
                cell.getTable().addRow({ project: null, description: "", hours: "" }, false); // false = add to bottom
              }
            }, 100);
          }
        }
      }
    ],
    cellEditing: function(cell) {
      // No need to clear placeholder, value is always empty string for empty
    },
    cellEdited: function(cell) {
      // If description is left empty, keep as empty string (formatter will show placeholder)
      if (cell.getField() === "description" && (!cell.getValue() || cell.getValue().trim() === "")) {
        cell.setValue("");
      }
      if (cell.getField() === "hours") {
        const val = Number(cell.getValue());
        if (!val || val <= 0) {
          alert("Please enter a number of hours greater than zero.");
          cell.setValue("");
        }
      }
      // Update summary bar immediately on edit
      updateSummaryBar();
      // Force a full table redraw so the X appears as soon as any field is filled
      table.redraw(true);
    }
  });

  setupDateControls();
  reloadGridForSelectedDate();
  document.getElementById("save-btn").addEventListener("click", saveGridData);

  // Add summary bar update on data load/change
  table.on("dataProcessed", updateSummaryBar);
  table.on("dataLoaded", updateSummaryBar);
}


function updateSummaryBar() {
  const data = table.getData();
  let totalHours = 0;
  for (let i = 0; i < data.length; i++) {
    const hours = parseFloat(data[i].hours) || 0;
    totalHours += hours;
  }
  let summary = document.getElementById("log-hours-summary");
  if (!summary) return;
  summary.textContent = `Total Daily Hours: ${totalHours}`;
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
        // Always use empty string for empty description
        let desc = row.description || row.WorkDescription || "";
        if (desc === "Enter description...") desc = "";
        // Always use empty string for empty hours
        let hrs = row.hours || row.WorkedHours || 0.0;
        if (!hrs || hrs === 0 || hrs === "0") hrs = "";
        return {
          project: project_id,
          description: desc,
          hours: hrs
        };
      });
    }
    // Always append a blank placeholder row for new entry
    mapped.push({
      project: null, // null so Tabulator select shows placeholder
      description: "",
      hours: ""
    });
    table.setData(mapped);
  } catch (err) {
    console.error("Fetch error loading logged hours:", err);
    alert("Could not load logged hours.");
  }
}

async function saveGridData() {
  const data = table.getData();

  // Exclude the last row if it's the placeholder (no project, no description, hours empty or 0)
  const filteredData = data.filter(row => row.project !== null || (row.description && row.description.trim() !== "") || (row.hours && Number(row.hours) !== 0));

  // Map project (id or label) to project_id and include the selected date
  const entries = filteredData.map(row => {
    let project_id = null;
    let project_label = null;
    if (typeof row.project === "number") {
      project_id = row.project;
      const found = projectOptions.find(opt => opt.value === row.project);
      if (found) project_label = found.label;
    } else if (typeof row.project === "string") {
      const projectObj = projectOptions.find(opt => opt.label === row.project);
      if (projectObj) {
        project_id = projectObj.value;
        project_label = projectObj.label;
      }
    }
    return {
      project_id,
      project_label,
      description: row.description && row.description.trim() ? row.description.trim() : null,
      hours: row.hours && !isNaN(Number(row.hours)) ? Number(row.hours) : null,
      date: selectedDate.toISOString().split('T')[0]
    };
  });

  // Filter out rows with missing required fields or hours <= 0
  const validEntries = entries.filter(e => e.project_id && e.description && e.hours !== null && e.hours !== "" && e.hours > 0);

  if (!validEntries.length && deletedRows.length === 0) {
    // Find the first invalid row for a more specific error
    const firstInvalid = entries.find(e => !e.project_id || !e.description || e.hours === null || e.hours === "" || e.hours <= 0);
    let msg = "Please select a project, enter a description, and enter hours greater than zero before saving.";
    if (firstInvalid) {
      if (!firstInvalid.project_id) msg = "Please choose a project.";
      else if (!firstInvalid.description) msg = "Please enter a description.";
      else if (firstInvalid.hours === null || firstInvalid.hours === "" || firstInvalid.hours <= 0) msg = "Please enter a valid number of hours greater than zero.";
    }
    alert(msg);
    return;
  }

  // Check for duplicate project entries for the same day (including already saved entries)
  // Get all loaded project IDs for the day (excluding placeholder row)
  const loadedRows = table.getData().filter(row => row.project !== null && row.project !== undefined && row.project !== "");
  const loadedProjectIds = loadedRows.map(row => (typeof row.project === "number") ? row.project : (projectOptions.find(opt => opt.label === row.project)?.value)).filter(Boolean);

  // For each entry being saved, if its project_id appears more than once in loadedProjectIds, warn
  const projectIdCounts = {};
  loadedProjectIds.forEach(pid => { projectIdCounts[pid] = (projectIdCounts[pid] || 0) + 1; });
  let duplicateEntry = null;
  for (const entry of validEntries) {
    if (projectIdCounts[entry.project_id] > 1) {
      duplicateEntry = entry;
      break;
    }
  }
  if (duplicateEntry) {
    const projectName = duplicateEntry.project_label || "this";
    const confirmMsg = `Are you sure you want to make multiple entries for the '${projectName}' project on this day?`;
    if (!window.confirm(confirmMsg)) {
      return;
    }
  }

  try {
    const response = await fetch("/submit_hours", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ consultant_id: consultantId, entries: validEntries, deleted: deletedRows })
    });

    const result = await response.json();
    // Custom message for delete-only actions
    if ((result.rows_inserted === 0 && result.rows_updated === 0) && result.rows_deleted > 0) {
      alert(`${result.rows_deleted} entr${result.rows_deleted === 1 ? 'y' : 'ies'} deleted.`);
    } else {
      alert(result.message || "Saved.");
    }

    // After successful save, reload grid and add a new placeholder row
    await reloadGridForSelectedDate();
    deletedRows = [];
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