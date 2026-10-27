(function () {
  function gapOf(rail) {
    var styles = window.getComputedStyle(rail);
    var raw = styles.columnGap;
    if (!raw || raw === "normal") {
      raw = styles.gap;
    }
    var gap = parseFloat(raw);
    return gap > 0 ? gap : 0;
  }

  function stepOf(rail) {
    var card = rail.querySelector(".review-card, .about-pick, .pop-card");
    if (!card) {
      return rail.clientWidth;
    }
    return card.getBoundingClientRect().width + gapOf(rail);
  }

  function bindRail(rail, prev, next) {
    if (!rail) {
      return;
    }

    function atEdges() {
      var max = rail.scrollWidth - rail.clientWidth;
      var left = rail.scrollLeft;
      if (prev) {
        prev.disabled = left <= 1;
      }
      if (next) {
        next.disabled = max <= 1 || left >= max - 1;
      }
    }

    function move(direction) {
      var distance = direction * stepOf(rail);
      var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      if (typeof rail.scrollBy === "function") {
        rail.scrollBy({ left: distance, behavior: reduce ? "auto" : "smooth" });
        return;
      }
      rail.scrollLeft += distance;
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
    rail.addEventListener("scroll", atEdges, { passive: true });
    window.addEventListener("resize", atEdges);
    window.addEventListener("load", atEdges);
    atEdges();
  }

  bindRail(
    document.querySelector("[data-reviews-track]"),
    document.querySelector("[data-about-reviews-prev]"),
    document.querySelector("[data-about-reviews-next]")
  );
  bindRail(
    document.querySelector("[data-about-pop]"),
    document.querySelector("[data-about-pop-prev]"),
    document.querySelector("[data-about-pop-next]")
  );
})();
