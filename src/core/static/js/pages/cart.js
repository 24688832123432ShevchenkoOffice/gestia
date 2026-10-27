document.addEventListener("click", (event) => {
  const button = event.target.closest("[data-qty-step], [data-qty-set]");
  if (!button) {
    return;
  }
  const form = button.closest("form");
  if (!form) {
    return;
  }
  const input = form.querySelector("[data-qty-input]");
  if (!input) {
    return;
  }
  if (button.hasAttribute("data-qty-set")) {
    input.value = button.getAttribute("data-qty-set") || "0";
  } else {
    const step = Number(button.getAttribute("data-qty-step"));
    const current = Number.parseInt(input.value, 10);
    const base = Number.isNaN(current) ? 1 : current;
    const next = Math.min(99, Math.max(1, base + step));
    input.value = String(next);
  }
  if (typeof form.requestSubmit === "function") {
    form.requestSubmit();
  } else {
    form.submit();
  }
});
