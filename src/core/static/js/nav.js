(function () {
  var header = document.querySelector("[data-header]");
  if (!header) return;

  var burgerBtn = header.querySelector("[data-burger]");
  var burger = document.querySelector("[data-burger-panel]");
  var catalogBtn = header.querySelector("[data-catalog]");
  var mega = header.querySelector("[data-mega]");
  var locale = header.querySelector("[data-locale]");
  var localeOpeners = document.querySelectorAll("[data-locale-open]");
  var scrollY = 0;

  function flag(node, open) {
    if (!node) return;
    node.hidden = !open;
  }

  function lock(open) {
    if (open) {
      scrollY = window.scrollY || window.pageYOffset || 0;
      document.body.classList.add("nav-lock");
      document.body.style.top = "-" + scrollY + "px";
      return;
    }
    document.body.classList.remove("nav-lock");
    document.body.style.top = "";
    window.scrollTo(0, scrollY);
  }

  function setBurger(open) {
    flag(burger, open);
    document.body.classList.toggle("is-burger", open);
    if (burgerBtn) burgerBtn.setAttribute("aria-expanded", open ? "true" : "false");
    if (open) setMega(false);
    lock(open);
  }

  function setMega(open) {
    flag(mega, open);
    document.body.classList.toggle("is-mega", open);
    if (catalogBtn) catalogBtn.setAttribute("aria-expanded", open ? "true" : "false");
  }

  function setLocale(open) {
    flag(locale, open);
    document.body.classList.toggle("is-locale", open);
    localeOpeners.forEach(function (button) {
      button.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  if (burgerBtn) {
    burgerBtn.addEventListener("click", function () {
      setBurger(burger.hidden);
    });
  }

  if (catalogBtn) {
    catalogBtn.addEventListener("click", function () {
      setLocale(false);
      setMega(mega.hidden);
    });
  }

  header.querySelectorAll("[data-catalog-close]").forEach(function (node) {
    node.addEventListener("click", function () {
      setMega(false);
    });
  });

  localeOpeners.forEach(function (button) {
    button.addEventListener("click", function () {
      setMega(false);
      setLocale(locale.hidden);
    });
  });

  header.querySelectorAll("[data-locale-close]").forEach(function (node) {
    node.addEventListener("click", function () {
      setLocale(false);
    });
  });

  document.addEventListener("keydown", function (event) {
    if (event.key !== "Escape") return;
    setMega(false);
    setLocale(false);
    if (burger && !burger.hidden) setBurger(false);
  });

  if (burger) {
    burger.addEventListener("click", function (event) {
      if (event.target.closest("a")) setBurger(false);
    });
  }
})();
