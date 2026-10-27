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

const sheet = document.querySelector("[data-catalog-sheet]");
const sheetBtn = document.querySelector("[data-sheet-open]");

function setSheet(open) {
  if (!sheet) {
    return;
  }
  sheet.hidden = !open;
  document.body.classList.toggle("filters-lock", open);
  if (sheetBtn) {
    sheetBtn.setAttribute("aria-expanded", open ? "true" : "false");
  }
}

if (frame && openBtn) {
  openBtn.addEventListener("click", () => {
    setOpen(!frame.classList.contains("is-filters"));
  });
  frame.addEventListener("click", (event) => {
    if (event.target.closest("[data-filters-close]")) {
      setOpen(false);
    }
  });
}

if (sheet && sheetBtn) {
  sheetBtn.addEventListener("click", () => {
    setSheet(sheet.hidden);
  });
  sheet.addEventListener("click", (event) => {
    if (event.target.closest("[data-sheet-close]")) {
      setSheet(false);
    }
  });
}

document.addEventListener("keydown", (event) => {
  if (event.key !== "Escape") {
    return;
  }
  if (frame && frame.classList.contains("is-filters")) {
    setOpen(false);
  }
  if (sheet && !sheet.hidden) {
    setSheet(false);
  }
});
