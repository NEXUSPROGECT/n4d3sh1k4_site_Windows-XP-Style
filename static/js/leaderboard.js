let leaderboardRequest = null;

function leaderboardLocale() {
  return document.documentElement.lang || "ru";
}

function renderLeaderboard(entries) {
  const body = document.getElementById("leaderboardBody");
  const table = document.getElementById("leaderboardTable");
  const empty = document.getElementById("leaderboardEmpty");
  const loading = document.getElementById("leaderboardLoading");
  if (!body || !table || !empty || !loading) return;

  body.textContent = "";

  entries.forEach((entry, index) => {
    const row = document.createElement("tr");

    const rank = document.createElement("td");
    rank.className = "leaderboard-rank";
    rank.textContent = String(entry.rank ?? index + 1);

    const name = document.createElement("td");
    name.textContent = String(entry.name ?? "");

    const score = document.createElement("td");
    score.className = "leaderboard-score";
    score.textContent = new Intl.NumberFormat(leaderboardLocale()).format(
      Number(entry.score) || 0,
    );

    const level = document.createElement("td");
    level.className = "leaderboard-level";
    level.textContent = String(entry.level ?? "");

    row.append(rank, name, score, level);
    body.appendChild(row);
  });

  const hasEntries = entries.length > 0;
  loading.hidden = true;
  table.hidden = !hasEntries;
  empty.hidden = hasEntries;
}

async function loadLeaderboard() {
  const loading = document.getElementById("leaderboardLoading");
  const empty = document.getElementById("leaderboardEmpty");
  const error = document.getElementById("leaderboardError");
  const table = document.getElementById("leaderboardTable");
  if (!loading || !empty || !error || !table) return;

  if (leaderboardRequest) return leaderboardRequest;

  loading.hidden = false;
  empty.hidden = true;
  error.hidden = true;
  table.hidden = true;

  leaderboardRequest = fetch("/api/leaderboard", {
    cache: "no-store",
    headers: { Accept: "application/json" },
  })
    .then((response) => {
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return response.json();
    })
    .then((data) => {
      renderLeaderboard(Array.isArray(data.entries) ? data.entries : []);
    })
    .catch(() => {
      loading.hidden = true;
      error.hidden = false;
    })
    .finally(() => {
      leaderboardRequest = null;
    });

  return leaderboardRequest;
}

function openLeaderboard() {
  if (typeof openWindow === "function") {
    openWindow("leaderboardWindow");
  }
  void loadLeaderboard();
}

// Load once for the mobile layout, where the window is always visible.
if (document.getElementById("leaderboardWindow")) {
  void loadLeaderboard();
}
