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

function deliveryMethodValue() {
  const checked = document.querySelector('input[name="delivery_method"]:checked');
  return checked ? checked.value : "np_branch";
}

function deliveryKind() {
  return deliveryMethodValue() === "np_locker" ? "locker" : "branch";
}

function isCourier() {
  return deliveryMethodValue() === "np_courier";
}

function splitStreetQuery(query) {
  const raw = (query || "").trim();
  const match = raw.match(
    /^(.+?)(?:,|\s)+(\d+[А-Яа-яA-Za-z]?(?:[/\-]\d+[А-Яа-яA-Za-z]?)?)\s*$/u
  );
  if (!match) {
    return { street: raw, house: "" };
  }
  return { street: match[1].trim(), house: match[2].trim() };
}

function initNpShip() {
  const root = document.querySelector("[data-np-ship]");
  if (!root) {
    return;
  }

  const cityInput = root.querySelector("[data-np-city]");
  const branchInput = root.querySelector("[data-np-branch]");
  const aptWrap = root.querySelector("[data-np-apt]");
  const aptInput = root.querySelector("[data-np-apartment]");
  const cityList = root.querySelector("#np-city-listbox");
  const branchList = root.querySelector("#np-branch-listbox");
  const hint = root.querySelector("[data-np-hint]");
  const arrow = root.querySelector("[data-np-arrow]");
  const secondWrap = root.querySelector("[data-np-second]");
  const streetLine = root.querySelector("[data-np-street-line]");
  if (!cityInput || !branchInput || !cityList || !branchList) {
    return;
  }

  const citiesUrl = root.dataset.npCitiesUrl || "";
  const warehousesUrl = root.dataset.npWarehousesUrl || "";
  const streetsUrl = root.dataset.npStreetsUrl || "";
  const minChars = Number(root.dataset.npMin || 2);
  const labelBranch = root.dataset.labelBranch || "Відділення";
  const labelLocker = root.dataset.labelLocker || "Поштомат";
  const labelStreet = root.dataset.labelStreet || "Вулиця, будинок";
  let cityTimer = 0;
  let streetTimer = 0;
  let cityRequest = 0;
  let branchRequest = 0;
  let streetRequest = 0;
  let cityRef = "";
  let warehouses = [];

  function syncSecondField() {
    const courier = isCourier();
    const locker = deliveryMethodValue() === "np_locker";
    branchInput.placeholder = courier ? labelStreet : locker ? labelLocker : labelBranch;
    branchInput.autocomplete = "off";
    branchInput.setAttribute("role", "combobox");
    branchInput.setAttribute("aria-autocomplete", "list");
    branchInput.setAttribute("aria-expanded", "false");
    branchInput.setAttribute("aria-controls", "np-branch-listbox");
    closeList(branchList, branchInput);
    warehouses = [];
    setHint("");
    if (arrow) {
      arrow.hidden = false;
    }
    if (secondWrap) {
      secondWrap.classList.toggle("is-courier", courier);
    }
    if (streetLine) {
      streetLine.classList.toggle("is-courier", courier);
    }
    if (aptWrap) {
      aptWrap.hidden = !courier;
    }
    if (aptInput && !courier) {
      aptInput.value = "";
    }
  }

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
          if (isCourier()) {
            branchInput.focus();
          } else {
            loadWarehouses();
            branchInput.focus();
          }
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
    if (isCourier() || !warehousesUrl || !cityRef) {
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

  async function loadStreets() {
    const { street, house } = splitStreetQuery(branchInput.value);
    if (!isCourier() || !streetsUrl || !cityRef || street.length < minChars) {
      if (isCourier()) {
        closeList(branchList, branchInput);
      }
      return;
    }

    const current = ++streetRequest;
    const url = new URL(streetsUrl, window.location.origin);
    url.searchParams.set("city_ref", cityRef);
    url.searchParams.set("q", street);

    try {
      const response = await fetch(url.toString(), {
        headers: { Accept: "application/json" },
        credentials: "same-origin",
      });
      const payload = await response.json().catch(() => ({}));
      if (current !== streetRequest) {
        return;
      }
      if (response.status === 503 || payload.error === "not_configured") {
        closeList(branchList, branchInput);
        setHint("Підказки вулиць тимчасово недоступні.");
        return;
      }
      if (!response.ok) {
        throw new Error(`streets ${response.status}`);
      }
      setHint("");
      const items = Array.isArray(payload.items) ? payload.items : [];
      openList(
        branchList,
        branchInput,
        items.map((item) => ({ label: item.label, ref: item.ref })),
        (row) => {
          branchInput.value = house ? `${row.label}, ${house}` : row.label;
          closeList(branchList, branchInput);
          if (aptInput) {
            aptInput.focus();
          }
        }
      );
      if (!items.length) {
        setHint("Вулиць не знайдено. Уточніть назву.");
      }
    } catch (_error) {
      if (current !== streetRequest) {
        return;
      }
      closeList(branchList, branchInput);
      setHint("Не вдалося завантажити вулиці.");
    }
  }

  function renderBranches(filterText) {
    if (isCourier()) {
      return;
    }
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

  function scheduleStreets() {
    window.clearTimeout(streetTimer);
    streetTimer = window.setTimeout(loadStreets, 280);
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

  branchInput.addEventListener("input", () => {
    if (isCourier()) {
      scheduleStreets();
      return;
    }
    renderBranches(branchInput.value);
  });
  branchInput.addEventListener("focus", () => {
    if (isCourier()) {
      if (!cityRef) {
        setHint("Спочатку оберіть місто зі списку.");
        return;
      }
      const { street } = splitStreetQuery(branchInput.value);
      if (street.length >= minChars) {
        scheduleStreets();
      } else {
        setHint("Вулиця зі списку, потім номер будинку. Квартиру — окремо.");
      }
      return;
    }
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
      if (aptInput) {
        aptInput.value = "";
      }
      warehouses = [];
      closeList(branchList, branchInput);
      syncSecondField();
      if (!isCourier() && cityRef) {
        loadWarehouses();
      }
    }
  });

  syncSecondField();
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
