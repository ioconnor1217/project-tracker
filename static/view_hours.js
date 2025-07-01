// view_hours.js
let selectedMonth = new Date();
let table;

async function getLoggedHours(year, month) {
  try {
    const res = await fetch(`/api/logged_hours?year=${year}&month=${month}`);
    if (!res.ok) {
      // If unauthorized, redirect to login, otherwise just return empty
      if (res.status === 403) {
        window.location.href = '/login';
        return [];
      }
      return [];
    }
    const data = await res.json();
    return data.data || [];
  } catch (e) {
    // On network or other error, just return empty
    return [];
  }
}

function setupMonthControls() {
  const monthPicker = document.getElementById("month-picker");
  // Set initial value to current month
  const pad = n => n < 10 ? "0" + n : n;
  monthPicker.value = `${selectedMonth.getFullYear()}-${pad(selectedMonth.getMonth() + 1)}`;
  monthPicker.addEventListener("change", () => {
    const [year, month] = monthPicker.value.split("-").map(Number);
    selectedMonth = new Date(year, month - 1, 1);
    reloadGridForSelectedMonth();
  });
  document.getElementById("prev-month").onclick = () => {
    selectedMonth.setMonth(selectedMonth.getMonth() - 1);
    monthPicker.value = `${selectedMonth.getFullYear()}-${pad(selectedMonth.getMonth() + 1)}`;
    reloadGridForSelectedMonth();
  };
  document.getElementById("next-month").onclick = () => {
    selectedMonth.setMonth(selectedMonth.getMonth() + 1);
    monthPicker.value = `${selectedMonth.getFullYear()}-${pad(selectedMonth.getMonth() + 1)}`;
    reloadGridForSelectedMonth();
  };
}

async function reloadGridForSelectedMonth() {
  const year = selectedMonth.getFullYear();
  const month = selectedMonth.getMonth() + 1;
  const data = await getLoggedHours(year, month);
  table.replaceData(data);
}

async function setupGrid() {
  table = new Tabulator("#view-hours-table", {
    layout: "fitColumns",
    placeholder: "No hours logged for this month.",
    columns: [
      {
        title: "Date",
        field: "date",
        sorter: "date",
        hozAlign: "center",
        formatter: function(cell) {
          let value = cell.getValue();
          if (!value) return "";
          let d = value instanceof Date ? value : new Date(value);
          if (isNaN(d)) return value;
          return d.toISOString().split("T")[0];
        }
      },
      { title: "Client", field: "client" },
      { title: "Project", field: "project" },
      { title: "Description", field: "description" },
      { title: "Hours", field: "hours", hozAlign: "right", bottomCalc: "sum", bottomCalcFormatter: function(cell) { return "Total Monthly Hours: " + cell.getValue(); } },
      { title: "Rate", field: "rate", hozAlign: "right", formatter: "money", formatterParams: { symbol: "$", precision: 2 }, bottomCalc: function(values, data) {
        // Calculate total bill for the month
        let total = 0;
        for (let i = 0; i < data.length; i++) {
          const hours = parseFloat(data[i].hours) || 0;
          const rate = parseFloat(data[i].rate) || 0;
          total += hours * rate;
        }
        return "Total Bill: $" + total.toFixed(2);
      } }
    ]
  });
  await reloadGridForSelectedMonth();
}

document.addEventListener("DOMContentLoaded", async () => {
  setupMonthControls();
  await setupGrid();
});
