(function () {
  const dialog = document.querySelector("[data-discount-modal]");
  if (!dialog || typeof dialog.showModal !== "function") {
    return;
  }

  const storageKey = dialog.dataset.storageKey || "gestia_discount_modal_shows";
  const delayMs = Math.max(0, Number(dialog.dataset.delayMs || 15000) || 0);
  const limit = Math.max(0, Number(dialog.dataset.shows || 1) || 0);
  let memoryCount = 0;
  let shown = false;
  let attempts = 0;

  function storedCount() {
    try {
      const parsed = Number(window.sessionStorage.getItem(storageKey));
      if (Number.isFinite(parsed) && parsed >= 0) {
        return parsed;
      }
    } catch (error) {
      return memoryCount;
    }
    return memoryCount;
  }

  function remember(next) {
    memoryCount = next;
    try {
      window.sessionStorage.setItem(storageKey, String(next));
    } catch (error) {
      /* приватний режим */
    }
  }

  function focusable() {
    const nodes = dialog.querySelectorAll(
      "a[href], button:not([disabled]), input:not([disabled]), textarea:not([disabled]), select:not([disabled]), [tabindex]:not([tabindex='-1'])"
    );
    return Array.prototype.filter.call(nodes, (node) => node.getClientRects().length > 0);
  }

  function trap(event) {
    if (event.key !== "Tab" || !dialog.open) {
      return;
    }
    const nodes = focusable();
    if (!nodes.length) {
      event.preventDefault();
      return;
    }
    const first = nodes[0];
    const last = nodes[nodes.length - 1];
    const active = document.activeElement;
    const inside = dialog.contains(active);
    if (event.shiftKey && (active === first || !inside)) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && (active === last || !inside)) {
      event.preventDefault();
      first.focus();
    }
  }

  function somethingElseOpen() {
    const openDialog = document.querySelector("dialog[open]");
    if (openDialog && openDialog !== dialog) {
      return true;
    }
    const waitlist = document.querySelector("[data-waitlist-modal]");
    return Boolean(waitlist && !waitlist.hidden);
  }

  function open() {
    if (shown || dialog.open || storedCount() >= limit) {
      return;
    }
    if (somethingElseOpen()) {
      if (attempts < 20) {
        attempts += 1;
        window.setTimeout(open, 1000);
      }
      return;
    }
    shown = true;
    const previous = document.activeElement;
    try {
      dialog.showModal();
    } catch (error) {
      shown = false;
      return;
    }
    remember(storedCount() + 1);
    const closeBtn = dialog.querySelector("[data-close-dialog]");
    if (closeBtn) {
      closeBtn.focus();
    }
    dialog.addEventListener(
      "close",
      function () {
        if (previous && typeof previous.focus === "function" && document.contains(previous)) {
          previous.focus();
        }
      },
      { once: true }
    );
  }

  dialog.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && dialog.open) {
      event.preventDefault();
      dialog.close();
      return;
    }
    trap(event);
  });
  window.setTimeout(open, delayMs);
})();
