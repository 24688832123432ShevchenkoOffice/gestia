if (window.htmx) {
  window.htmx.config.responseHandling = [
    { code: "204", swap: false },
    { code: "[23]..", swap: true },
    { code: "422", swap: true },
    { code: "429", swap: true },
    { code: "[45]..", swap: false, error: true },
  ];
}

document.body.addEventListener("htmx:configRequest", (event) => {
  const meta = document.querySelector('meta[name="csrf-token"]');
  if (meta) {
    event.detail.headers["X-CSRFToken"] = meta.content;
  }
});
