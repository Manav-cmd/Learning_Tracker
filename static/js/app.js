// ======================================================
// APP.JS — SINGLE SOURCE OF TRUTH
// ======================================================

document.addEventListener("DOMContentLoaded", () => {
  setupTheme();
  setupProgressChart();
});

// ======================================================
// THEME TOGGLE (NO INLINE JS, NO DUPLICATES)
// ======================================================

function setupTheme() {
  const root = document.documentElement;
  const toggleBtn = document.getElementById("themeToggle");

  // Load saved theme or default to dark
  const savedTheme = localStorage.getItem("theme") || "dark";
  root.dataset.theme = savedTheme;

  if (!toggleBtn) return;

  toggleBtn.addEventListener("click", () => {
    const nextTheme =
      root.dataset.theme === "dark" ? "light" : "dark";

    root.dataset.theme = nextTheme;
    localStorage.setItem("theme", nextTheme);
  });
}

// ======================================================
// PROGRESS DASHBOARD CHART (SAFE + OPTIONAL)
// ======================================================

function setupProgressChart() {
  const canvas = document.getElementById("progressChart");

  // Chart only exists on progress page
  if (!canvas) return;

  // These MUST be injected by view_progress.html
  if (
    typeof completedCount === "undefined" ||
    typeof inProgressCount === "undefined" ||
    typeof notStartedCount === "undefined"
  ) {
    console.warn("Progress counts not found. Chart skipped.");
    return;
  }

  const ctx = canvas.getContext("2d");

  new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: ["Completed", "In Progress", "Not Started"],
      datasets: [
        {
          data: [
            completedCount,
            inProgressCount,
            notStartedCount
          ],
          backgroundColor: [
            "#22c55e",
            "#facc15",
            "#94a3b8"
          ],
          borderWidth: 2,
          borderColor: "#0b1220"
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: "70%",
      plugins: {
        legend: {
          position: "bottom",
          labels: {
            color:
              document.documentElement.dataset.theme === "dark"
                ? "#e5e7eb"
                : "#0f172a",
            font: { size: 13 }
          }
        }
      }
    }
  });
}
