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

  // Calculate totals
  let totalHours = 0;
  let totalBill = 0;
  data.forEach(row => {
    totalHours += Number(row.hours) || 0;
    totalBill += (Number(row.hours) || 0) * (Number(row.rate) || 0);
  });
  document.getElementById('monthly-hours').textContent = `Total Monthly Hours: ${totalHours}`;
  document.getElementById('monthly-bill').textContent = `Total Bill: $${totalBill.toFixed(2)}`;
}

async function setupGrid() {
  table = new Tabulator("#view-hours-table", {
    layout: "fitDataTable",
    responsiveLayout: false,
    placeholder: "No hours logged for this month.",
    autoColumns: false,
    columns: [
      {
        title: "Date",
        field: "date",
        sorter: "date",
        hozAlign: "center",
        formatter: function(cell) {
          let value = cell.getValue();
          if (!value) return "";
          let d = new Date(value);
          if (isNaN(d)) return value;
          return d.toISOString().split("T")[0];
        }
      },
      { title: "Client", field: "client" },
      { title: "Project", field: "project" },
      { title: "Description", field: "description" },
      { title: "Hours", field: "hours", hozAlign: "right" },
      { title: "Rate", field: "rate", hozAlign: "right", formatter: "money", formatterParams: { symbol: "$", precision: 2 } }
    ]
  });
  await reloadGridForSelectedMonth();
  updateSummaryBar();
  table.on("dataProcessed", updateSummaryBar);
}

function updateSummaryBar() {
  const data = table.getData();
  let totalHours = 0;
  let totalBill = 0;
  for (let i = 0; i < data.length; i++) {
    const hours = parseFloat(data[i].hours) || 0;
    const rate = parseFloat(data[i].rate) || 0;
    totalHours += hours;
    totalBill += hours * rate;
  }

  let summary = document.getElementById("view-hours-summary");
  if (!summary) {
    summary = document.createElement("div");
    summary.id = "view-hours-summary";
    summary.style.margin = "18px 0 0 0";
    summary.style.fontWeight = "600";
    summary.style.fontSize = "1.1em";
    summary.style.color = "#4A90E2";
    document.getElementById("view-hours-table").parentNode.appendChild(summary);
  }
  summary.innerHTML = `<div id="monthly-hours">Total Monthly Hours: ${totalHours}</div><div id="monthly-bill">Total Bill: $${totalBill.toFixed(2)}</div>`;
}

document.addEventListener("DOMContentLoaded", function() {
  setupMonthControls();
  setupGrid();
  const exportBtn = document.getElementById('export-csv');
  if (exportBtn) {
    exportBtn.addEventListener('click', function() {
      if (table) {
        const year = selectedMonth.getFullYear();
        const month = (selectedMonth.getMonth() + 1).toString().padStart(2, '0');
        const filename = `monthly_hours_${year}-${month}.csv`;
        // Get table data and filter out 'rate' and 'client', add 'Day' column
        const data = table.getData().map(row => {
          const {date, project, description, hours} = row;
          let day = '';
          if (date) {
            const d = new Date(date);
            if (!isNaN(d)) {
              day = d.toLocaleDateString('en-US', { weekday: 'long' });
            }
          }
          return {day, date, project, description, hours};
        });
        // Convert to CSV
        const csvRows = ["Day,Date,Hours,Project,Description"];
        data.forEach(row => {
          csvRows.push(`"${row.day}","${row.date}","${row.hours}","${row.project}","${row.description}"`);
        });
        const csvContent = csvRows.join("\n");
        // Download CSV
        const blob = new Blob([csvContent], {type: 'text/csv'});
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      }
    });
  }
});
