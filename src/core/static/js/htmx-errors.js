(function () {
  var timer = 0;

  function root() {
    return document.querySelector("[data-net-toast-root]");
  }

  function messageFor(event) {
    var node = root();
    if (!node) {
      return "";
    }
    if (event.type === "htmx:sendError") {
      return node.getAttribute("data-offline") || "";
    }
    return node.getAttribute("data-error") || "";
  }

  function show(text) {
    if (!text || !document.body) {
      return;
    }
    var toast = document.querySelector("body > .net-toast");
    if (!toast) {
      toast = document.createElement("div");
      toast.className = "net-toast";
      toast.setAttribute("role", "status");
      toast.setAttribute("aria-live", "polite");
      document.body.appendChild(toast);
    }
    toast.hidden = false;
    toast.textContent = text;
    window.clearTimeout(timer);
    timer = window.setTimeout(function () {
      toast.hidden = true;
    }, 4000);
  }

  function onError(event) {
    var xhr = event.detail && event.detail.xhr;
    if (xhr && xhr.status === 422) {
      return;
    }
    show(messageFor(event));
  }

  document.addEventListener("htmx:sendError", onError);
  document.addEventListener("htmx:responseError", onError);
})();
