function clampQty(value) {
  const number = Number.parseInt(value, 10);
  if (Number.isNaN(number)) {
    return 1;
  }
  return Math.min(99, Math.max(1, number));
}

function bindQty(root) {
  const input = root.querySelector("[data-qty]");
  const label = root.querySelector("[data-qty-label]");
  if (!input || !label) {
    return;
  }
  function setQty(next) {
    const value = String(clampQty(next));
    input.value = value;
    label.textContent = value;
  }
  const inc = root.querySelector("[data-qty-inc]");
  const dec = root.querySelector("[data-qty-dec]");
  if (inc) {
    inc.addEventListener("click", () => setQty(Number(input.value) + 1));
  }
  if (dec) {
    dec.addEventListener("click", () => setQty(Number(input.value) - 1));
  }
}

function bindGallery(gallery) {
  const shots = Array.from(gallery.querySelectorAll("[data-shot]"));
  if (shots.length < 2) {
    return;
  }
  let index = Math.max(0, shots.findIndex((shot) => shot.classList.contains("is-current")));

  function show(next) {
    index = (next + shots.length) % shots.length;
    shots.forEach((shot, shotIndex) => {
      shot.classList.toggle("is-current", shotIndex === index);
    });
  }

  const prev = gallery.querySelector("[data-pdp-prev]");
  const next = gallery.querySelector("[data-pdp-next]");
  if (prev) {
    prev.addEventListener("click", () => show(index - 1));
  }
  if (next) {
    next.addEventListener("click", () => show(index + 1));
  }
}

function bindRail(bar) {
  const rail = bar.parentElement && bar.parentElement.querySelector(".pdp-rail--mob");
  if (!rail) {
    return;
  }
  const step = 188;
  const prev = bar.querySelector("[data-rail-prev]");
  const next = bar.querySelector("[data-rail-next]");
  if (prev) {
    prev.addEventListener("click", () => {
      rail.scrollBy({ left: -step, behavior: "smooth" });
    });
  }
  if (next) {
    next.addEventListener("click", () => {
      rail.scrollBy({ left: step, behavior: "smooth" });
    });
  }
}

document.querySelectorAll("[data-pdp]").forEach((root) => {
  bindQty(root);
  const gallery = root.querySelector("[data-pdp-gallery]");
  if (gallery) {
    bindGallery(gallery);
  }
  root.querySelectorAll("[data-pdp-more]").forEach(bindRail);
});
