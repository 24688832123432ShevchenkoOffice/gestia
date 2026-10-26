const toggle = document.querySelector("[data-menu-open]");
const nav = document.querySelector("[data-site-nav]");

if (toggle && nav) {
  toggle.addEventListener("click", () => {
    const open = nav.classList.toggle("is-open");
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    document.body.classList.toggle("nav-lock", open);
  });

  nav.addEventListener("click", (event) => {
    if (event.target.closest("a") && nav.classList.contains("is-open")) {
      nav.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
      document.body.classList.remove("nav-lock");
    }
  });
}
