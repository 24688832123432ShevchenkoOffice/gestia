const frame = document.querySelector("[data-catalog-page]");
const openBtn = document.querySelector("[data-filters-open]");

function setOpen(open) {
  if (!frame) {
    return;
  }
  frame.classList.toggle("is-filters", open);
  const closed = frame.querySelector("[data-catalog-closed]");
  const panel = frame.querySelector("[data-catalog-open]");
  if (closed) {
    closed.hidden = open;
  }
  if (panel) {
    panel.hidden = !open;
  }
  if (openBtn) {
    openBtn.setAttribute("aria-expanded", open ? "true" : "false");
  }
}

if (frame && openBtn) {
  openBtn.addEventListener("click", () => {
    const open = !frame.classList.contains("is-filters");
    setOpen(open);
  });
  frame.addEventListener("click", (event) => {
    if (event.target.closest("[data-filters-close]")) {
      setOpen(false);
    }
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && frame.classList.contains("is-filters")) {
      setOpen(false);
    }
  });
}
