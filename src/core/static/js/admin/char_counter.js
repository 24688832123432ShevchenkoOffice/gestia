(function () {
  "use strict";

  var SKIP = {
    hidden: 1,
    file: 1,
    checkbox: 1,
    radio: 1,
    button: 1,
    submit: 1,
    color: 1,
    range: 1,
    password: 1,
  };

  function maxOf(field) {
    var max = parseInt(field.getAttribute("maxlength"), 10);
    return max > 0 ? max : 0;
  }

  function clamp(field, max) {
    if (field.value.length <= max) return;
    var pos = field.selectionStart;
    field.value = field.value.slice(0, max);
    if (typeof pos === "number" && field.setSelectionRange) {
      var next = Math.min(pos, max);
      try {
        field.setSelectionRange(next, next);
      } catch (error) {
        return;
      }
    }
  }

  function paint(field, counter, max) {
    var length = field.value.length;
    counter.textContent = length + " / " + max;
    counter.classList.toggle("is-warn", length >= Math.floor(max * 0.9));
  }

  function place(field, counter) {
    var parent = field.parentNode;
    if (parent && parent !== document.body && parent.children.length <= 3) {
      parent.insertAdjacentElement("afterend", counter);
      return;
    }
    field.insertAdjacentElement("afterend", counter);
  }

  function bindField(field) {
    if (!field || field.dataset.gestiaCount === "1") return;
    if (field.closest && field.closest(".tox-tinymce")) return;
    var type = (field.getAttribute("type") || "").toLowerCase();
    if (SKIP[type]) return;
    var max = maxOf(field);
    if (!max) return;
    field.dataset.gestiaCount = "1";
    field.setAttribute("maxlength", String(max));

    var counter = document.createElement("span");
    counter.className = "gestia-char-count";
    counter.setAttribute("aria-live", "polite");
    place(field, counter);

    function update() {
      clamp(field, max);
      paint(field, counter, max);
    }

    field.addEventListener("beforeinput", function (event) {
      if (!event.inputType || event.inputType.indexOf("delete") === 0) return;
      var data = event.data || "";
      if (!data) return;
      var start = field.selectionStart;
      var end = field.selectionEnd;
      if (start == null || end == null) return;
      var room = max - (field.value.length - (end - start));
      if (data.length <= room) return;
      event.preventDefault();
      if (room > 0 && field.setRangeText) {
        field.setRangeText(data.slice(0, room), start, end, "end");
      }
      update();
    });
    field.addEventListener("input", update);
    field.addEventListener("paste", function () {
      window.setTimeout(update, 0);
    });
    update();
  }

  function bind(root) {
    var scope = root || document;
    scope.querySelectorAll("input[maxlength], textarea[maxlength]").forEach(bindField);
  }

  function start() {
    bind(document);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }

  document.addEventListener("formset:added", function (event) {
    bind(event.target || document);
  });
})();
