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

function closeSortMenus(except) {
  document.querySelectorAll("[data-catalog-sort]").forEach((root) => {
    if (except && root === except) {
      return;
    }
    const menu = root.querySelector("[data-sort-menu]");
    const btn = root.querySelector("[data-sort-open]");
    if (menu) {
      menu.hidden = true;
    }
    root.classList.remove("is-open");
    if (btn) {
      btn.setAttribute("aria-expanded", "false");
    }
  });
}

function applySort(value) {
  const url = new URL(window.location.href);
  if (value) {
    url.searchParams.set("sort", value);
  } else {
    url.searchParams.delete("sort");
  }
  window.location.assign(url.pathname + url.search + url.hash);
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

document.addEventListener("click", (event) => {
  const opener = event.target.closest("[data-sort-open]");
  if (opener) {
    const root = opener.closest("[data-catalog-sort]");
    if (!root) {
      return;
    }
    const menu = root.querySelector("[data-sort-menu]");
    const open = menu && menu.hidden;
    closeSortMenus(root);
    if (menu) {
      menu.hidden = !open;
    }
    root.classList.toggle("is-open", Boolean(open));
    opener.setAttribute("aria-expanded", open ? "true" : "false");
    return;
  }

  const option = event.target.closest("[data-sort-value]");
  if (option) {
    event.preventDefault();
    applySort(option.getAttribute("data-sort-value") || "");
    return;
  }

  if (!event.target.closest("[data-catalog-sort]")) {
    closeSortMenus();
  }
});

document.addEventListener("keydown", (event) => {
  if (event.key !== "Escape") {
    return;
  }
  closeSortMenus();
  if (frame && frame.classList.contains("is-filters")) {
    setOpen(false);
  }
  if (sheet && !sheet.hidden) {
    setSheet(false);
  }
});
