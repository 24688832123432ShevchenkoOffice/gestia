const gallery = document.querySelector("[data-gallery]");
if (gallery) {
  const main = gallery.querySelector("[data-gallery-main]");
  const thumbs = Array.from(gallery.querySelectorAll("[data-gallery-thumb]"));
  let index = 0;

  function show(next) {
    if (!thumbs.length || !main) {
      return;
    }
    index = (next + thumbs.length) % thumbs.length;
    main.src = thumbs[index].getAttribute("data-full");
  }

  thumbs.forEach((thumb, thumbIndex) => {
    thumb.addEventListener("click", () => show(thumbIndex));
  });

  const prev = gallery.querySelector("[data-gallery-prev]");
  const next = gallery.querySelector("[data-gallery-next]");
  if (prev) {
    prev.addEventListener("click", () => show(index - 1));
  }
  if (next) {
    next.addEventListener("click", () => show(index + 1));
  }
}
