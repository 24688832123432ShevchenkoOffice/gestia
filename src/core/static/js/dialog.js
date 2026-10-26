document.addEventListener("click", (event) => {
  const opener = event.target.closest("[data-open-dialog]");
  if (opener) {
    const dialog = document.getElementById(opener.getAttribute("data-open-dialog"));
    if (dialog && typeof dialog.showModal === "function") {
      dialog.showModal();
    }
  }
  const closer = event.target.closest("[data-close-dialog]");
  if (closer) {
    const dialog = closer.closest("dialog");
    if (dialog) {
      dialog.close();
    }
  }
});
