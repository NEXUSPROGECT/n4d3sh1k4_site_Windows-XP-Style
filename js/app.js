let zIndex = 10;
const taskbar = document.getElementById("taskbarWindows");
const openWindows = new Map();

/* ---------- HELPERS ---------- */
function constrainWindowPosition(win) {
  // Skip if window is hidden
  if (win.style.display === "none") return;
  
  const desktop = document.querySelector(".desktop");
  const padding = 10;
  const computedStyle = window.getComputedStyle(win);
  
  let left = parseFloat(computedStyle.left);
  let top = parseFloat(computedStyle.top);
  
  const width = win.offsetWidth;
  const height = win.offsetHeight;
  
  // Constrain left
  if (left < padding) left = padding;
  if (left + width > desktop.offsetWidth - padding) {
    left = desktop.offsetWidth - width - padding;
  }
  
  // Constrain top
  if (top < padding) top = padding;
  if (top + height > desktop.offsetHeight - padding - 40) {
    top = desktop.offsetHeight - height - padding - 40;
  }
  
  win.style.left = left + "px";
  win.style.top = top + "px";
  win.style.right = "auto";
}

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
  
  const titleSpan = win.querySelector(".title-bar-text span[data-i18n]");
  if (titleSpan) {
    const span = document.createElement("span");
    span.setAttribute("data-i18n", titleSpan.getAttribute("data-i18n"));
    span.textContent = titleSpan.textContent;
    btn.appendChild(span);
  } else {
    btn.textContent = win.dataset.title;
  }

  btn.onclick = () => {
    if (win.style.display === "none") {
      win.style.display = "block";
    }
    focusWindow(win);
  };

  taskbar.appendChild(btn);
  openWindows.set(win.id, btn);
  btn.classList.add("active");
  
  if (typeof applyTranslations === "function") {
    applyTranslations();
  }
}

function removeTaskbarButton(id) {
  const btn = openWindows.get(id);
  if (btn) btn.remove();
  openWindows.delete(id);
}

/* ---------- DRAGGABLE & RESIZABLE WINDOWS ---------- */
let activeWindow = null;
let dragging = false, resizing = false;
let resizeMode = null;
let startX, startY, startWidth, startHeight, startLeft, startTop;

document.querySelectorAll(".window").forEach(win => {
  const titleBar = win.querySelector(".title-bar");

  // Drag functionality
  titleBar.addEventListener("mousedown", e => {
    if (dragging || resizing) return;
    dragging = true;
    activeWindow = win;
    focusWindow(win);
    const computedStyle = window.getComputedStyle(win);
    startLeft = parseFloat(computedStyle.left);
    startTop = parseFloat(computedStyle.top);
    startX = e.clientX;
    startY = e.clientY;
  });

  // Resize handles
  const createResizeHandle = (position) => {
    const handle = document.createElement("div");
    handle.className = `resize-handle resize-${position}`;
    win.appendChild(handle);
    
    handle.addEventListener("mousedown", (e) => {
      if (dragging || resizing) return;
      e.preventDefault();
      e.stopPropagation();
      
      // Save all values first, before any other operations
      resizing = true;
      resizeMode = position;
      activeWindow = win;
      startX = e.clientX;
      startY = e.clientY;
      startWidth = win.offsetWidth;
      startHeight = win.offsetHeight;
      const computedStyle = window.getComputedStyle(win);
      startLeft = parseFloat(computedStyle.left);
      startTop = parseFloat(computedStyle.top);
      
      // Focus window last
      focusWindow(win);
    });
  };

  // Create all resize handles (corners and edges)
  ["nw", "n", "ne", "e", "se", "s", "sw", "w"].forEach(pos => {
    createResizeHandle(pos);
  });
});

// Global mousemove listener
document.addEventListener("mousemove", e => {
  if (!activeWindow) return;
  
  if (dragging) {
    const deltaX = e.clientX - startX;
    const deltaY = e.clientY - startY;
    activeWindow.style.left = (startLeft + deltaX) + "px";
    activeWindow.style.top = (startTop + deltaY) + "px";
    activeWindow.style.right = "auto";
  }
  
  if (resizing) {
    const deltaX = e.clientX - startX;
    const deltaY = e.clientY - startY;
    
    // Set minimum sizes based on window content
    let minWidth, minHeight;
    switch (activeWindow.id) {
      case 'profileWindow':
        // Avatar (152px) + text + padding
        minWidth = 280;
        minHeight = 195;
        break;
      case 'aboutWindow':
        // Notepad text display area
        minWidth = 352;
        minHeight = 154;
        break;
      case 'projectsWindow':
        // Grid (max-width 450px) + divider (2px) + preview pane
        minWidth = 650;
        minHeight = 350;
        break;
      default:
        minWidth = 250;
        minHeight = 150;
    }

    let newWidth = startWidth;
    let newHeight = startHeight;
    let newLeft = startLeft;
    let newTop = startTop;

    // Handle width changes
    if (resizeMode.includes("e")) {
      newWidth = Math.max(minWidth, startWidth + deltaX);
    }
    if (resizeMode.includes("w")) {
      const constrainedWidth = Math.max(minWidth, startWidth - deltaX);
      const actualDeltaWidth = startWidth - constrainedWidth;
      newWidth = constrainedWidth;
      newLeft = startLeft + actualDeltaWidth;
    }

    // Handle height changes
    if (resizeMode.includes("s")) {
      newHeight = Math.max(minHeight, startHeight + deltaY);
    }
    if (resizeMode.includes("n")) {
      const constrainedHeight = Math.max(minHeight, startHeight - deltaY);
      const actualDeltaHeight = startHeight - constrainedHeight;
      newHeight = constrainedHeight;
      newTop = startTop + actualDeltaHeight;
    }

    activeWindow.style.width = newWidth + "px";
    activeWindow.style.height = newHeight + "px";
    activeWindow.style.left = newLeft + "px";
    activeWindow.style.top = newTop + "px";
  }
});

// Global mouseup listener
document.addEventListener("mouseup", () => {
  if (activeWindow) {
    if (dragging || resizing) {
      constrainWindowPosition(activeWindow);
    }
    dragging = false;
    resizing = false;
    resizeMode = null;
    activeWindow = null;
  }
});

// Update cursor on hover
document.querySelectorAll(".window").forEach(win => {
  win.addEventListener("mousemove", (e) => {
    if (!dragging && !resizing) {
      const rect = win.getBoundingClientRect();
      const edge = 8;
      let cursor = "default";

      const top = e.clientY - rect.top < edge;
      const bottom = e.clientY - rect.bottom > -edge;
      const left = e.clientX - rect.left < edge;
      const right = e.clientX - rect.right > -edge;

      if ((top && left) || (bottom && right)) cursor = "nwse-resize";
      else if ((top && right) || (bottom && left)) cursor = "nesw-resize";
      else if (top || bottom) cursor = "ns-resize";
      else if (left || right) cursor = "ew-resize";

      win.style.cursor = cursor;
    }
  });
});

/* ---------- CLOCK ---------- */
function updateClock() {
  const now = new Date();
  document.getElementById("clock").textContent =
    now.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}
setInterval(updateClock, 1000);
updateClock();

/* ---------- INITIALIZE WINDOW LAYOUT ---------- */
function initializeWindowLayout() {
  const viewport = document.querySelector(".viewport");
  const viewportWidth = viewport.clientWidth;
  const viewportHeight = viewport.clientHeight;
  
  // Skip on mobile (viewport width <= 768px) - CSS handles mobile layout with !important
  if (viewportWidth <= 768) {
    return;
  }
  
  const padding = 20;
  const centerX = viewportWidth / 2;
  const centerY = viewportHeight / 2;

  // Define windows with their preferred sizes and minimum constraints
  const windowConfigs = {
    profileWindow: {
      width: Math.min(307, viewportWidth * 0.3),
      height: Math.min(200, viewportHeight * 0.25),
      offsetX: -450, // Offset from center
      offsetY: -250,
      minWidth: 280,
      minHeight: 195
    },
    aboutWindow: {
      width: Math.min(380, viewportWidth * 0.35),
      height: Math.min(300, viewportHeight * 0.15),
      offsetX: -130,  // Offset from center
      offsetY: -250,
      minWidth: 352,
      minHeight: 154
    },
    projectsWindow: {
      width: Math.min(700, viewportWidth * 0.85),
      height: Math.min(360, viewportHeight * 0.65),
      offsetX: -450, // Center horizontally
      offsetY: -40,   // Below other windows
      minWidth: 650,
      minHeight: 350
    }
  };

  Object.entries(windowConfigs).forEach(([id, config]) => {
    const win = document.getElementById(id);
    if (win) {
      // Apply minimum size constraints
      const finalWidth = Math.max(config.width, config.minWidth);
      const finalHeight = Math.max(config.height, config.minHeight);
      
      // Calculate centered position
      let left = centerX + config.offsetX;
      let top = centerY + config.offsetY;

      // Constrain to viewport
      left = Math.max(padding, Math.min(left, viewportWidth - finalWidth - padding));
      top = Math.max(padding, Math.min(top, viewportHeight - finalHeight - padding - 40));

      // Apply styles
      win.style.width = Math.round(finalWidth) + "px";
      win.style.height = Math.round(finalHeight) + "px";
      win.style.left = Math.round(left) + "px";
      win.style.top = Math.round(top) + "px";
      win.style.right = "auto";
    }
  });
}

/* ---------- AUTO RESIZE ON WINDOW CHANGE ---------- */
function autoResizeWindows() {
  document.querySelectorAll(".window").forEach(win => {
    if (win.style.display !== "none") {
      constrainWindowPosition(win);
    }
  });
}

window.addEventListener("resize", autoResizeWindows);
// Initial check
setTimeout(() => {
  initializeWindowLayout();
  autoResizeWindows();
}, 100);

/* ---------- PROJECTS ---------- */
let projectTranslations = {};

// Load projects data and translations
async function loadProjects() {
  try {
    const projectsRes = await fetch("projects.json");
    const projects = await projectsRes.json();
    
    const projectsTransRes = await fetch(`i18n/projects.${currentLang}.json`);
    projectTranslations = await projectsTransRes.json();

    initializeProjects(projects);
  } catch (error) {
    console.error("Error loading projects:", error);
  }
}

function initializeProjects(projects) {
  const list = document.getElementById("projectsList");
  const preview = document.getElementById("projectsPreview");
  
  // Clear previous projects to prevent duplication on reload
  list.innerHTML = "";
  preview.innerHTML = '<div class="preview-empty" data-i18n="projects.empty">Select a project to view details</div>';
  
  let currentProjectIndex = -1;
  let currentScreenshot = 0;

  const showPreview = (projectIndex) => {
    const p = projects[projectIndex];
    const lastWord = p.linkType ? p.linkType.split(" ").pop() : "link";
    currentProjectIndex = projectIndex;
    currentScreenshot = 0;

    const projectKey = p.id;
    const projectTitle = projectTranslations[`project.${projectKey}.title`] || projectKey;
    const projectDesc = projectTranslations[`project.${projectKey}.description`] || "";

    const mobileClass = p.isMobileApp ? " mobile" : "";
    const firstScreenshot = p.screenshots && p.screenshots.length > 0 ? p.screenshots[0] : p.preview;
    
    const previewHTML = `
      <div class="preview-content">
        <div class="preview-image-container${mobileClass}">
          <div class="preview-image${mobileClass}" style="background-image: url('${firstScreenshot}')"></div>
          ${p.screenshots.length > 1 ? `
            <div class="preview-controls">
              <button class="preview-nav-btn" onclick="prevScreenshot(${projectIndex})">❮</button>
              <div class="preview-counter"><span id="current-screenshot">1</span>/${p.screenshots.length}</div>
              <button class="preview-nav-btn" onclick="nextScreenshot(${projectIndex})">❯</button>
            </div>
          ` : ''}\
        </div>
        <div class="preview-title">${projectTitle}</div>
        <div class="preview-type">${p.linkType || "Link"}</div>
        <div class="preview-description">${projectDesc}</div>
        <button class="preview-button" onclick="window.open('${p.url}', '_blank')">Open ${lastWord}</button>
      </div>
    `;
    
    preview.innerHTML = previewHTML;
      
      // Ресайз контейнера для мобильных приложений
      if (p.isMobileApp) {
        const img = new Image();
        img.onload = () => {
          const aspectRatio = img.width / img.height;
          const container = preview.querySelector(".preview-image-container.mobile");
          if (container) {
            if (aspectRatio < 0.5) {
              // Более узкий экран - немного сужаем
              container.style.maxWidth = "270px";
            } else if (aspectRatio > 0.65) {
              // Более широкий экран - немного расширяем
              container.style.maxWidth = "330px";
            } else {
              container.style.maxWidth = "300px";
            }
          }
        };
        img.src = p.preview;
      }
    };

    window.nextScreenshot = (projectIndex) => {
      const p = projects[projectIndex];
      currentScreenshot = (currentScreenshot + 1) % p.screenshots.length;
      const imageEl = preview.querySelector(".preview-image");
      imageEl.style.backgroundImage = `url('${p.screenshots[currentScreenshot]}')`;
      const counter = document.getElementById("current-screenshot");
      if (counter) counter.textContent = currentScreenshot + 1;
      
      if (p.isMobileApp) {
        const img = new Image();
        img.onload = () => {
          const aspectRatio = img.width / img.height;
          const container = preview.querySelector(".preview-image-container.mobile");
          if (container) {
            if (aspectRatio < 0.5) {
              container.style.maxWidth = "270px";
            } else if (aspectRatio > 0.65) {
              container.style.maxWidth = "330px";
            } else {
              container.style.maxWidth = "300px";
            }
          }
        };
        img.src = p.screenshots[currentScreenshot];
      }
    };

    window.prevScreenshot = (projectIndex) => {
      const p = projects[projectIndex];
      currentScreenshot = (currentScreenshot - 1 + p.screenshots.length) % p.screenshots.length;
      const imageEl = preview.querySelector(".preview-image");
      imageEl.style.backgroundImage = `url('${p.screenshots[currentScreenshot]}')`;
      const counter = document.getElementById("current-screenshot");
      if (counter) counter.textContent = currentScreenshot + 1;
      
      if (p.isMobileApp) {
        const img = new Image();
        img.onload = () => {
          const aspectRatio = img.width / img.height;
          const container = preview.querySelector(".preview-image-container.mobile");
          if (container) {
            if (aspectRatio < 0.5) {
              container.style.maxWidth = "270px";
            } else if (aspectRatio > 0.65) {
              container.style.maxWidth = "330px";
            } else {
              container.style.maxWidth = "300px";
            }
          }
        };
        img.src = p.screenshots[currentScreenshot];
      }
    };

    projects.forEach((p, index) => {
      const projectKey = p.id;
      const projectTitle = projectTranslations[`project.${projectKey}.title`] || projectKey;
      
      const thumbnail = document.createElement("div");
      thumbnail.className = "project-thumbnail";
      thumbnail.dataset.index = index;
      
      const lastWord = p.linkType ? p.linkType.split(" ").pop() : "link";
      thumbnail.title = projectTitle + "\nClick to view details";

      const imageDiv = document.createElement("div");
      imageDiv.className = "project-thumbnail-image";
      imageDiv.style.backgroundImage = `url(${p.preview})`;

      const nameDiv = document.createElement("div");
      nameDiv.className = "project-thumbnail-name";
      nameDiv.textContent = projectTitle;

      thumbnail.appendChild(imageDiv);
      thumbnail.appendChild(nameDiv);
      
      thumbnail.onclick = (e) => {
        e.stopPropagation();
        document.querySelectorAll(".project-thumbnail").forEach(t => {
          t.classList.remove("selected");
        });
        thumbnail.classList.add("selected");
        showPreview(index);
      };

      list.appendChild(thumbnail);
    });
    
    // Ensure windows are within bounds after page load
    setTimeout(() => {
      document.querySelectorAll(".window").forEach(win => {
        constrainWindowPosition(win);
      });
    }, 250);
    
    // Apply translations in case static strings (like preview-empty) were added
    if (typeof applyTranslations === "function") {
      applyTranslations();
    }
}

// Load projects when page loads
loadProjects();

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