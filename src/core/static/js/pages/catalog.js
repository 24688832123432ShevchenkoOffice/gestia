const panel = document.getElementById("filters");
const openBtn = document.querySelector("[data-filters-open]");

function closePanel() {
  if (!panel) {
    return;
  }
  panel.classList.remove("is-open");
  panel.setAttribute("aria-hidden", "true");
  document.body.classList.remove("nav-lock");
  if (openBtn) {
    openBtn.setAttribute("aria-expanded", "false");
  }
}

if (panel && openBtn) {
  closePanel();
  openBtn.addEventListener("click", () => {
    panel.classList.add("is-open");
    panel.removeAttribute("aria-hidden");
    document.body.classList.add("nav-lock");
    openBtn.setAttribute("aria-expanded", "true");
  });
  panel.addEventListener("click", (event) => {
    if (event.target.closest("[data-filters-close]")) {
      closePanel();
    }
  });
}
