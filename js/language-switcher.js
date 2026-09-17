function switchLanguage(lang) {
  document.cookie = "lang=" + lang + "; path=/; max-age=31536000; SameSite=Lax";
  loadLang(lang);
}