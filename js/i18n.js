let currentLang = localStorage.getItem("lang") || "ru";
let translations = {};

async function loadLang(lang) {
  currentLang = lang; // Fix: Update global language state
  const res = await fetch(`i18n/${lang}.json`);
  translations = await res.json();
  applyTranslations();
  localStorage.setItem("lang", lang);
  
  // Reload project translations when language changes
  if (typeof loadProjects === 'function') {
    await loadProjects();
  }
}

function applyTranslations() {
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.dataset.i18n;
    if (translations[key]) {
      el.textContent = translations[key];
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  loadLang(currentLang);
});
