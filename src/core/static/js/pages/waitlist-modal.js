(function () {
  const root = document.querySelector("[data-waitlist-modal]");
  if (!root) {
    return;
  }

  const storageKey = root.dataset.storageKey || "gestia_waitlist_modal_seen";
  const startedKey = root.dataset.startedKey || "gestia_waitlist_site_started_at";
  const delayMs = Number(root.dataset.delayMs || 15000);
  let timerId = 0;
  let lastFocused = null;

  function alreadySeen() {
    try {
      return window.sessionStorage.getItem(storageKey) === "1";
    } catch (_error) {
      return false;
    }
  }

  function markSeen() {
    try {
      window.sessionStorage.setItem(storageKey, "1");
    } catch (_error) {
      /* ignore */
    }
  }

  function startedAt() {
    try {
      const raw = window.sessionStorage.getItem(startedKey);
      const parsed = Number(raw);
      if (parsed > 0) {
        return parsed;
      }
      const now = Date.now();
      window.sessionStorage.setItem(startedKey, String(now));
      return now;
    } catch (_error) {
      return Date.now();
    }
  }

  function openModal() {
    if (alreadySeen() || root.classList.contains("is-open")) {
      return;
    }
    markSeen();
    lastFocused = document.activeElement;
    root.hidden = false;
    requestAnimationFrame(() => {
      root.classList.add("is-open");
    });
    document.body.classList.add("waitlist-modal-open");
    const closeBtn = root.querySelector(".waitlist-modal__close");
    if (closeBtn) {
      closeBtn.focus();
    }
  }

  function closeModal() {
    if (!root.classList.contains("is-open") && root.hidden) {
      return;
    }
    markSeen();
    root.classList.remove("is-open");
    document.body.classList.remove("waitlist-modal-open");
    window.setTimeout(() => {
      root.hidden = true;
    }, 280);
    if (lastFocused && typeof lastFocused.focus === "function") {
      lastFocused.focus();
    }
  }

  root.addEventListener("click", (event) => {
    if (event.target.closest("[data-waitlist-close]")) {
      closeModal();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && root.classList.contains("is-open")) {
      closeModal();
    }
  });

  document.body.addEventListener("htmx:afterSwap", (event) => {
    if (event.target && event.target.id === "waitlist-form-slot") {
      markSeen();
    }
  });

  if (alreadySeen()) {
    return;
  }

  const remaining = Math.max(0, delayMs - (Date.now() - startedAt()));
  timerId = window.setTimeout(openModal, remaining);
  window.addEventListener(
    "pagehide",
    () => {
      window.clearTimeout(timerId);
    },
    { once: true }
  );
})();
