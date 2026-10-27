function markChoice(name) {
  const inputs = document.querySelectorAll(`input[name="${name}"]`);
  inputs.forEach((input) => {
    const label = input.closest("label");
    if (!label) {
      return;
    }
    label.classList.toggle("is-on", input.checked);
  });
}

function syncChoices() {
  markChoice("delivery_method");
  markChoice("payment_method");
}

function deliveryKind() {
  const checked = document.querySelector('input[name="delivery_method"]:checked');
  return checked && checked.value === "np_locker" ? "locker" : "branch";
}

function initNpShip() {
  const root = document.querySelector("[data-np-ship]");
  if (!root) {
    return;
  }

  const cityInput = root.querySelector("[data-np-city]");
  const branchInput = root.querySelector("[data-np-branch]");
  const listbox = root.querySelector("#np-branch-listbox");
  if (!cityInput || !branchInput || !listbox) {
    return;
  }

  const endpoint = branchInput.dataset.autocompleteEndpoint || "";
  const minChars = Number(branchInput.dataset.autocompleteMin || 2);
  let items = [];
  let timer = 0;
  let requestId = 0;

  function setExpanded(open) {
    branchInput.setAttribute("aria-expanded", open ? "true" : "false");
    listbox.hidden = !open;
  }

  function render(filterText) {
    const needle = (filterText || "").trim().toLocaleLowerCase("uk");
    const visible = needle
      ? items.filter((item) => item.label.toLocaleLowerCase("uk").includes(needle))
      : items;

    listbox.replaceChildren();
    if (!visible.length) {
      setExpanded(false);
      return;
    }

    visible.forEach((item, index) => {
      const option = document.createElement("li");
      option.className = "co-branch-list__item";
      option.setAttribute("role", "option");
      option.id = `np-branch-option-${index}`;
      option.tabIndex = -1;
      option.textContent = item.label;
      option.addEventListener("mousedown", (event) => {
        event.preventDefault();
        branchInput.value = item.label;
        setExpanded(false);
      });
      listbox.appendChild(option);
    });
    setExpanded(true);
  }

  async function loadWarehouses() {
    const query = cityInput.value.trim();
    if (!endpoint || query.length < minChars) {
      items = [];
      setExpanded(false);
      return;
    }

    const current = ++requestId;
    const url = new URL(endpoint, window.location.origin);
    url.searchParams.set("q", query);
    url.searchParams.set("kind", deliveryKind());

    try {
      const response = await fetch(url.toString(), {
        headers: { Accept: "application/json" },
        credentials: "same-origin",
      });
      if (!response.ok) {
        throw new Error(`np ${response.status}`);
      }
      const payload = await response.json();
      if (current !== requestId) {
        return;
      }
      items = Array.isArray(payload.items) ? payload.items : [];
      if (payload.city && query.length <= payload.city.length) {
        const official = String(payload.city);
        if (official && !cityInput.value.includes(",")) {
          cityInput.dataset.npResolved = official;
        }
      }
      render(branchInput.value);
    } catch (_error) {
      if (current !== requestId) {
        return;
      }
      items = [];
      setExpanded(false);
    }
  }

  function scheduleLoad() {
    window.clearTimeout(timer);
    timer = window.setTimeout(loadWarehouses, 300);
  }

  cityInput.addEventListener("input", scheduleLoad);
  cityInput.addEventListener("change", scheduleLoad);
  branchInput.addEventListener("input", () => render(branchInput.value));
  branchInput.addEventListener("focus", () => {
    if (items.length) {
      render(branchInput.value);
    } else {
      scheduleLoad();
    }
  });
  branchInput.addEventListener("blur", () => {
    window.setTimeout(() => setExpanded(false), 120);
  });

  document.addEventListener("change", (event) => {
    const input = event.target;
    if (input && input.name === "delivery_method") {
      branchInput.value = "";
      scheduleLoad();
    }
  });

  if (cityInput.value.trim().length >= minChars) {
    scheduleLoad();
  }
}

document.addEventListener("change", (event) => {
  const input = event.target;
  if (!input || !input.name) {
    return;
  }
  if (input.name === "delivery_method" || input.name === "payment_method") {
    markChoice(input.name);
  }
});

document.addEventListener("DOMContentLoaded", () => {
  syncChoices();
  initNpShip();
});
