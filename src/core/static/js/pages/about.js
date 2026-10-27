(function () {
  var rail = document.querySelector("[data-about-pop]");
  if (!rail) {
    return;
  }
  var prev = document.querySelector("[data-about-pop-prev]");
  var next = document.querySelector("[data-about-pop-next]");

  function step() {
    var card = rail.querySelector(".about-pick, .pop-card");
    if (!card) {
      return rail.clientWidth;
    }
    var raw = window.getComputedStyle(rail).columnGap;
    var gap = parseFloat(raw);
    if (!gap) {
      gap = 14;
    }
    return card.getBoundingClientRect().width + gap;
  }

  function move(direction) {
    var left = direction * step();
    var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (typeof rail.scrollBy === "function") {
      rail.scrollBy({ left: left, behavior: reduce ? "auto" : "smooth" });
      return;
    }
    rail.scrollLeft += left;
  }

  if (prev) {
    prev.addEventListener("click", function () {
      move(-1);
    });
  }
  if (next) {
    next.addEventListener("click", function () {
      move(1);
    });
  }
})();
