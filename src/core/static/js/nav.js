(function () {
  var header = document.querySelector("[data-header]");
  if (!header) return;

  var burgerBtn = header.querySelector("[data-burger]");
  var burger = document.querySelector("[data-burger-panel]");
  var catalogBtn = header.querySelector("[data-catalog]");
  var mega = header.querySelector("[data-mega]");
  var scrollY = 0;
  var locked = false;

  function flag(node, open) {
    if (!node) return;
    node.hidden = !open;
  }

  function lock(open) {
    if (open) {
      if (locked) return;
      locked = true;
      scrollY = window.scrollY || window.pageYOffset || 0;
      document.body.classList.add("nav-lock");
      document.body.style.top = "-" + scrollY + "px";
      return;
    }
    if (!locked) return;
    locked = false;
    document.body.classList.remove("nav-lock");
    document.body.style.top = "";
    window.scrollTo(0, scrollY);
  }

  function setBurger(open) {
    flag(burger, open);
    document.body.classList.toggle("is-burger", open);
    if (burgerBtn) burgerBtn.setAttribute("aria-expanded", open ? "true" : "false");
    if (open) {
      flag(mega, false);
      document.body.classList.remove("is-mega");
      if (catalogBtn) catalogBtn.setAttribute("aria-expanded", "false");
    }
    lock(open || (mega && !mega.hidden));
  }

  function setMega(open) {
    flag(mega, open);
    document.body.classList.toggle("is-mega", open);
    if (catalogBtn) catalogBtn.setAttribute("aria-expanded", open ? "true" : "false");
    if (open) {
      flag(burger, false);
      document.body.classList.remove("is-burger");
      if (burgerBtn) burgerBtn.setAttribute("aria-expanded", "false");
    }
    lock(open || (burger && !burger.hidden));
  }

  function closeSwitches(except) {
    document.querySelectorAll("[data-switch]").forEach(function (root) {
      if (except && root === except) return;
      var menu = root.querySelector("[data-switch-menu]");
      var trigger = root.querySelector("[data-switch-open]");
      if (menu) menu.hidden = true;
      root.classList.remove("is-open");
      if (trigger) trigger.setAttribute("aria-expanded", "false");
    });
  }

  function toggleSwitch(root) {
    var menu = root.querySelector("[data-switch-menu]");
    var trigger = root.querySelector("[data-switch-open]");
    if (!menu || !trigger) return;
    var open = menu.hidden;
    closeSwitches(root);
    menu.hidden = !open;
    root.classList.toggle("is-open", open);
    trigger.setAttribute("aria-expanded", open ? "true" : "false");
  }

  if (burgerBtn) {
    burgerBtn.addEventListener("click", function () {
      closeSwitches();
      setBurger(burger.hidden);
    });
  }

  if (catalogBtn) {
    catalogBtn.addEventListener("click", function () {
      closeSwitches();
      setMega(mega.hidden);
    });
  }

  header.querySelectorAll("[data-catalog-close]").forEach(function (node) {
    node.addEventListener("click", function () {
      setMega(false);
    });
  });

  document.addEventListener("click", function (event) {
    var opener = event.target.closest("[data-switch-open]");
    if (opener) {
      event.preventDefault();
      setMega(false);
      toggleSwitch(opener.closest("[data-switch]"));
      return;
    }
    if (!event.target.closest("[data-switch]")) {
      closeSwitches();
    }
  });

  document.addEventListener("keydown", function (event) {
    if (event.key !== "Escape") return;
    setMega(false);
    closeSwitches();
    if (burger && !burger.hidden) setBurger(false);
  });

  if (burger) {
    burger.addEventListener("click", function (event) {
      var toggle = event.target.closest("[data-burger-catalog-toggle]");
      if (toggle) {
        var block = toggle.closest("[data-burger-catalog]");
        if (!block) return;
        var open = toggle.getAttribute("aria-expanded") !== "true";
        block.classList.toggle("is-collapsed", !open);
        toggle.setAttribute("aria-expanded", open ? "true" : "false");
        return;
      }
      if (event.target.closest("a")) setBurger(false);
    });
  }

  if (mega) {
    mega.addEventListener("click", function (event) {
      if (event.target.closest("a")) setMega(false);
    });
  }

  window.addEventListener(
    "scroll",
    function () {
      if (mega && !mega.hidden) setMega(false);
    },
    { passive: true }
  );
})();
