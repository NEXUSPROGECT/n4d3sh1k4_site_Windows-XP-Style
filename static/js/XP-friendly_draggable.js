let activeWindow = null;
let offsetX = 0;
let offsetY = 0;
let windowZ = 10;

const desktop = document.getElementById("desktop");

document.addEventListener("mousedown", e => {
  const titleBar = e.target.closest(".title-bar");
  if (!titleBar) return;

  activeWindow = titleBar.closest(".window");
  if (!activeWindow || activeWindow.id === "loader") return;

  activeWindow.style.zIndex = ++windowZ;

  const rect = activeWindow.getBoundingClientRect();
  offsetX = e.clientX - rect.left;
  offsetY = e.clientY - rect.top;

  document.body.style.userSelect = "none";
});

document.addEventListener("mousemove", e => {
  if (!activeWindow) return;

  const deskRect = desktop.getBoundingClientRect();
  const winRect = activeWindow.getBoundingClientRect();

  let x = e.clientX - offsetX - deskRect.left;
  let y = e.clientY - offsetY - deskRect.top;

  const maxX = deskRect.width - winRect.width;
  const maxY = deskRect.height - winRect.height;

  x = Math.max(0, Math.min(x, maxX));
  y = Math.max(0, Math.min(y, maxY));

  activeWindow.style.left = x + "px";
  activeWindow.style.top = y + "px";
});

document.addEventListener("mouseup", () => {
  activeWindow = null;
  document.body.style.userSelect = "";
});
