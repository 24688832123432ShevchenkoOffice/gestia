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
  const cityList = root.querySelector("#np-city-listbox");
  const branchList = root.querySelector("#np-branch-listbox");
  const hint = root.querySelector("[data-np-hint]");
  if (!cityInput || !branchInput || !cityList || !branchList) {
    return;
  }

  const citiesUrl = root.dataset.npCitiesUrl || "";
  const warehousesUrl = root.dataset.npWarehousesUrl || "";
  const minChars = Number(root.dataset.npMin || 2);
  let cityTimer = 0;
  let cityRequest = 0;
  let branchRequest = 0;
  let cityRef = "";
  let warehouses = [];

  function setHint(text) {
    if (!hint) {
      return;
    }
    if (!text) {
      hint.hidden = true;
      hint.textContent = "";
      return;
    }
    hint.hidden = false;
    hint.textContent = text;
  }

  function closeList(list, input) {
    list.hidden = true;
    list.replaceChildren();
    if (input) {
      input.setAttribute("aria-expanded", "false");
    }
  }

  function openList(list, input, rows, onPick) {
    list.replaceChildren();
    if (!rows.length) {
      closeList(list, input);
      return;
    }
    rows.forEach((row, index) => {
      const option = document.createElement("li");
      option.className = "co-suggest__item";
      option.setAttribute("role", "option");
      option.id = `${list.id}-opt-${index}`;
      option.textContent = row.label;
      option.addEventListener("mousedown", (event) => {
        event.preventDefault();
        onPick(row);
      });
      list.appendChild(option);
    });
    list.hidden = false;
    input.setAttribute("aria-expanded", "true");
  }

  async function loadCities() {
    const query = cityInput.value.trim();
    cityRef = "";
    warehouses = [];
    closeList(branchList, branchInput);
    if (!citiesUrl || query.length < minChars) {
      closeList(cityList, cityInput);
      setHint("");
      return;
    }

    const current = ++cityRequest;
    const url = new URL(citiesUrl, window.location.origin);
    url.searchParams.set("q", query);

    try {
      const response = await fetch(url.toString(), {
        headers: { Accept: "application/json" },
        credentials: "same-origin",
      });
      const payload = await response.json().catch(() => ({}));
      if (current !== cityRequest) {
        return;
      }
      if (response.status === 503 || payload.error === "not_configured") {
        closeList(cityList, cityInput);
        setHint("Підказки Нової пошти тимчасово недоступні. Додайте API-ключ.");
        return;
      }
      if (!response.ok) {
        throw new Error(`cities ${response.status}`);
      }
      setHint("");
      const items = Array.isArray(payload.items) ? payload.items : [];
      openList(
        cityList,
        cityInput,
        items.map((item) => ({ label: item.name, ref: item.ref, name: item.name })),
        (row) => {
          cityInput.value = row.name;
          cityRef = row.ref;
          closeList(cityList, cityInput);
          branchInput.value = "";
          loadWarehouses();
          branchInput.focus();
        }
      );
    } catch (_error) {
      if (current !== cityRequest) {
        return;
      }
      closeList(cityList, cityInput);
      setHint("Не вдалося завантажити міста. Спробуйте ще раз.");
    }
  }

  async function loadWarehouses() {
    if (!warehousesUrl || !cityRef) {
      warehouses = [];
      closeList(branchList, branchInput);
      return;
    }

    const current = ++branchRequest;
    const url = new URL(warehousesUrl, window.location.origin);
    url.searchParams.set("city_ref", cityRef);
    url.searchParams.set("kind", deliveryKind());

    try {
      const response = await fetch(url.toString(), {
        headers: { Accept: "application/json" },
        credentials: "same-origin",
      });
      const payload = await response.json().catch(() => ({}));
      if (current !== branchRequest) {
        return;
      }
      if (!response.ok) {
        throw new Error(`warehouses ${response.status}`);
      }
      warehouses = Array.isArray(payload.items) ? payload.items : [];
      renderBranches(branchInput.value);
      if (!warehouses.length) {
        setHint("Для цього міста відділень не знайдено.");
      } else {
        setHint("");
      }
    } catch (_error) {
      if (current !== branchRequest) {
        return;
      }
      warehouses = [];
      closeList(branchList, branchInput);
      setHint("Не вдалося завантажити відділення.");
    }
  }

  function renderBranches(filterText) {
    const needle = (filterText || "").trim().toLocaleLowerCase("uk");
    const rows = warehouses
      .filter((item) => !needle || item.label.toLocaleLowerCase("uk").includes(needle))
      .map((item) => ({ label: item.label, ref: item.ref }));
    openList(branchList, branchInput, rows, (row) => {
      branchInput.value = row.label;
      closeList(branchList, branchInput);
    });
  }

  function scheduleCities() {
    window.clearTimeout(cityTimer);
    cityTimer = window.setTimeout(loadCities, 280);
  }

  cityInput.addEventListener("input", () => {
    cityRef = "";
    scheduleCities();
  });
  cityInput.addEventListener("focus", () => {
    if (cityInput.value.trim().length >= minChars && cityList.childElementCount) {
      cityList.hidden = false;
      cityInput.setAttribute("aria-expanded", "true");
    } else {
      scheduleCities();
    }
  });
  cityInput.addEventListener("blur", () => {
    window.setTimeout(() => closeList(cityList, cityInput), 140);
  });

  branchInput.addEventListener("input", () => renderBranches(branchInput.value));
  branchInput.addEventListener("focus", () => {
    if (warehouses.length) {
      renderBranches(branchInput.value);
    } else if (cityRef) {
      loadWarehouses();
    } else if (cityInput.value.trim().length >= minChars) {
      setHint("Спочатку оберіть місто зі списку.");
    }
  });
  branchInput.addEventListener("blur", () => {
    window.setTimeout(() => closeList(branchList, branchInput), 140);
  });

  document.addEventListener("change", (event) => {
    const input = event.target;
    if (input && input.name === "delivery_method") {
      branchInput.value = "";
      warehouses = [];
      closeList(branchList, branchInput);
      if (cityRef) {
        loadWarehouses();
      }
    }
  });
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
