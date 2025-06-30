// view_hours.js
let selectedMonth = new Date();
let table;

async function getLoggedHours(year, month) {
  const res = await fetch(`/api/logged_hours?year=${year}&month=${month}`);
  const data = await res.json();
  return data.data || [];
}

function setupMonthControls() {
  const monthDisplay = document.getElementById("month-display");
  function updateDisplay() {
    monthDisplay.textContent = selectedMonth.toLocaleString("default", { month: "long", year: "numeric" });
  }
  document.getElementById("prev-month").onclick = () => {
    selectedMonth.setMonth(selectedMonth.getMonth() - 1);
    updateDisplay();
    reloadGridForSelectedMonth();
  };
  document.getElementById("next-month").onclick = () => {
    selectedMonth.setMonth(selectedMonth.getMonth() + 1);
    updateDisplay();
    reloadGridForSelectedMonth();
  };
  updateDisplay();
}

async function reloadGridForSelectedMonth() {
  const year = selectedMonth.getFullYear();
  const month = selectedMonth.getMonth() + 1;
  const data = await getLoggedHours(year, month);
  table.replaceData(data);
}

async function setupGrid() {
  table = new Tabulator("#view-hours-table", {
    height: 400,
    layout: "fitColumns",
    placeholder: "No hours logged for this month.",
    columns: [
      { title: "Date", field: "date", sorter: "date", hozAlign: "center" },
      { title: "Client", field: "client" },
      { title: "Project", field: "project" },
      { title: "Description", field: "description" },
      { title: "Hours", field: "hours", hozAlign: "right" }
    ]
  });
  await reloadGridForSelectedMonth();
}

document.addEventListener("DOMContentLoaded", async () => {
  setupMonthControls();
  await setupGrid();
});
