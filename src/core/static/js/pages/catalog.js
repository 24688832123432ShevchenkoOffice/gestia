const panel = document.getElementById("filters");
const openBtn = document.querySelector("[data-filters-open]");
const desktop = window.matchMedia("(min-width: 900px)");

function sync() {
  if (!panel) {
    return;
  }
  if (desktop.matches) {
    panel.classList.remove("is-open");
    panel.removeAttribute("aria-hidden");
    document.body.classList.remove("nav-lock");
  } else if (!panel.classList.contains("is-open")) {
    panel.setAttribute("aria-hidden", "true");
  }
}

if (panel && openBtn) {
  openBtn.addEventListener("click", () => {
    panel.classList.add("is-open");
    panel.removeAttribute("aria-hidden");
    document.body.classList.add("nav-lock");
  });
  panel.addEventListener("click", (event) => {
    if (event.target.closest("[data-filters-close]")) {
      panel.classList.remove("is-open");
      panel.setAttribute("aria-hidden", "true");
      document.body.classList.remove("nav-lock");
    }
  });
  desktop.addEventListener("change", sync);
  sync();
}
