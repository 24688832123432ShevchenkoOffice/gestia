(function () {
  function normalize(value, fallback) {
    var raw = String(value || "").trim();
    if (!raw) {
      return fallback;
    }
    if (raw.charAt(0) !== "#") {
      raw = "#" + raw;
    }
    if (/^#[0-9a-fA-F]{3}$/.test(raw)) {
      raw = "#" + raw.charAt(1) + raw.charAt(1) + raw.charAt(2) + raw.charAt(2) + raw.charAt(3) + raw.charAt(3);
    }
    if (!/^#[0-9a-fA-F]{6}$/.test(raw)) {
      return fallback;
    }
    return raw.toLowerCase();
  }

  function paint(root, value, notify) {
    var native = root.querySelector("[data-gestia-color-native]");
    var hex = root.querySelector("[data-gestia-color-hex]");
    var fallback = root.getAttribute("data-default-color") || "#241c16";
    var next = normalize(value, fallback);
    if (!native) {
      return;
    }
    if (native.value !== next) {
      native.value = next;
    }
    if (hex && hex.value.toLowerCase() !== next) {
      hex.value = next;
    }
    if (!notify) {
      return;
    }
    native.dispatchEvent(new Event("input", { bubbles: true }));
    native.dispatchEvent(new Event("change", { bubbles: true }));
  }

  function bind(root) {
    if (!root || root.getAttribute("data-gestia-color-bound") === "1") {
      return;
    }
    root.setAttribute("data-gestia-color-bound", "1");
    var native = root.querySelector("[data-gestia-color-native]");
    var hex = root.querySelector("[data-gestia-color-hex]");
    var reset = root.querySelector("[data-gestia-color-reset]");
    var fallback = root.getAttribute("data-default-color") || "#241c16";
    if (!native) {
      return;
    }
    native.addEventListener("input", function () {
      paint(root, native.value, false);
    });
    if (hex) {
      hex.addEventListener("change", function () {
        paint(root, hex.value || fallback, true);
      });
    }
    if (reset) {
      reset.addEventListener("click", function (event) {
        event.preventDefault();
        paint(root, fallback, true);
      });
    }
    paint(root, native.value || fallback, false);
  }

  function boot() {
    document.querySelectorAll("[data-gestia-color]").forEach(bind);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
