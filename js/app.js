let zIndex = 10;
const taskbar = document.getElementById("taskbarWindows");
const openWindows = new Map();

/* ---------- WINDOW MANAGEMENT ---------- */
function openWindow(id) {
  const win = document.getElementById(id);
  win.style.display = "block";
  focusWindow(win);

  if (!openWindows.has(id)) {
    createTaskbarButton(win);
  }
}

function closeWindow(id) {
  const win = document.getElementById(id);
  win.style.display = "none";
  removeTaskbarButton(id);
}

function focusWindow(win) {
  zIndex++;
  win.style.zIndex = zIndex;

  document.querySelectorAll(".taskbar-window-btn")
    .forEach(b => b.classList.remove("active"));

  const btn = openWindows.get(win.id);
  if (btn) btn.classList.add("active");
}

/* ---------- TASKBAR ---------- */
function createTaskbarButton(win) {
  const btn = document.createElement("button");
  btn.className = "taskbar-window-btn";
  btn.textContent = win.dataset.title;

  btn.onclick = () => {
    if (win.style.display === "none") {
      win.style.display = "block";
    }
    focusWindow(win);
  };

  taskbar.appendChild(btn);
  openWindows.set(win.id, btn);
  btn.classList.add("active");
}

function removeTaskbarButton(id) {
  const btn = openWindows.get(id);
  if (btn) btn.remove();
  openWindows.delete(id);
}

/* ---------- DRAGGABLE WINDOWS ---------- */
document.querySelectorAll(".window").forEach(win => {
  const titleBar = win.querySelector(".title-bar");
  let offsetX = 0, offsetY = 0, dragging = false;

  titleBar.addEventListener("mousedown", e => {
    dragging = true;
    focusWindow(win);
    offsetX = e.clientX - win.offsetLeft;
    offsetY = e.clientY - win.offsetTop;
  });

  document.addEventListener("mousemove", e => {
    if (!dragging) return;
    win.style.left = e.clientX - offsetX + "px";
    win.style.top = e.clientY - offsetY + "px";
  });

  document.addEventListener("mouseup", () => dragging = false);
});

/* ---------- CLOCK ---------- */
function updateClock() {
  const now = new Date();
  document.getElementById("clock").textContent =
    now.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}
setInterval(updateClock, 1000);
updateClock();

/* ---------- PROJECTS ---------- */
fetch("projects.json")
  .then(r => r.json())
  .then(projects => {
    const list = document.getElementById("projectsList");
    projects.forEach(p => {
      const thumbnail = document.createElement("div");
      thumbnail.className = "project-thumbnail";
      thumbnail.title = p.title + "\nClick to open GitHub";

      const imageDiv = document.createElement("div");
      imageDiv.className = "project-thumbnail-image";
      imageDiv.style.backgroundImage = `url(${p.screenshots[0]})`;

      const nameDiv = document.createElement("div");
      nameDiv.className = "project-thumbnail-name";
      nameDiv.textContent = p.title;

      thumbnail.appendChild(imageDiv);
      thumbnail.appendChild(nameDiv);
      
      thumbnail.onclick = () => window.open(p.url, "_blank");

      list.appendChild(thumbnail);
    });
  });

const startMenu = document.getElementById("startMenu");
function toggleStart() {
  startMenu.style.display =
    startMenu.style.display === "block" ? "none" : "block";
}



document.addEventListener("click", e => {
  if (!e.target.closest(".start-menu") &&
      !e.target.closest(".start-button")) {
    startMenu.style.display = "none";
  }
});