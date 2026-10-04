/* TrevorGames site script: video play buttons and the screenshot lightbox.
   No trackers, no cookies, no storage. Everything works without it:
   videos keep their native controls and screenshots open as plain links. */
(function () {
  "use strict";

  var PLAY_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M7 4.5v15l12.5-7.5z" fill="currentColor"/></svg>';
  var ICONS = {
    prev: '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M15 5l-7 7 7 7" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    next: '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M9 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    close: '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 6l12 12M18 6L6 18" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>'
  };

  /* ---------- Video: one big play button over the poster ---------- */
  var videos = [];
  document.querySelectorAll(".player").forEach(function (player) {
    var video = player.querySelector("video");
    if (!video) return;
    videos.push(video);
    /* Hide the native control bar until playback starts, so the poster stays clean. */
    video.removeAttribute("controls");
    var label = player.getAttribute("data-label") || "Play video";
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "play-btn";
    btn.setAttribute("aria-label", label);
    btn.innerHTML = PLAY_ICON;
    player.appendChild(btn);

    btn.addEventListener("click", function () {
      player.classList.add("is-started");
      video.setAttribute("controls", "");
      var p = video.play();
      if (p && p.catch) p.catch(function () { player.classList.remove("is-started"); });
      video.focus({ preventScroll: true });
    });
    video.addEventListener("play", function () {
      player.classList.add("is-started");
      video.setAttribute("controls", "");
      videos.forEach(function (other) { if (other !== video && !other.paused) other.pause(); });
    });
  });

  /* ---------- Lightbox for .gallery ---------- */
  var gallery = document.querySelector("[data-lightbox]");
  if (!gallery || typeof HTMLDialogElement !== "function") return;

  var links = Array.prototype.slice.call(gallery.querySelectorAll("a.shot"));
  if (!links.length) return;

  var dlg = document.createElement("dialog");
  dlg.className = "lightbox";
  dlg.setAttribute("aria-label", "Screenshot viewer");
  dlg.innerHTML =
    '<div class="lb-top"><p class="lb-count" aria-live="polite"></p>' +
    '<button type="button" class="lb-btn lb-close" aria-label="Close">' + ICONS.close + '</button></div>' +
    '<div class="lb-stage"><img alt="" decoding="async">' +
    '<button type="button" class="lb-btn lb-prev" aria-label="Previous screenshot">' + ICONS.prev + '</button>' +
    '<button type="button" class="lb-btn lb-next" aria-label="Next screenshot">' + ICONS.next + '</button></div>' +
    '<p class="lb-caption"></p>';
  document.body.appendChild(dlg);

  var img = dlg.querySelector("img");
  var count = dlg.querySelector(".lb-count");
  var caption = dlg.querySelector(".lb-caption");
  var stage = dlg.querySelector(".lb-stage");
  var index = 0;
  var opener = null;

  function show(i) {
    index = (i + links.length) % links.length;
    var a = links[index];
    var thumb = a.querySelector("img");
    img.src = a.getAttribute("href");
    img.alt = thumb ? thumb.alt : "";
    caption.textContent = thumb ? thumb.alt : "";
    count.textContent = "Screenshot " + (index + 1) + " of " + links.length;
    var next = links[(index + 1) % links.length];
    var pre = new Image();
    pre.src = next.getAttribute("href");
  }

  function open(i, from) {
    opener = from || null;
    show(i);
    document.documentElement.classList.add("lb-open");
    dlg.showModal();
    dlg.querySelector(".lb-next").focus();
  }

  dlg.addEventListener("close", function () {
    document.documentElement.classList.remove("lb-open");
    img.removeAttribute("src");
    if (opener) opener.focus();
  });

  links.forEach(function (a, i) {
    a.addEventListener("click", function (e) {
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.button === 1) return;
      e.preventDefault();
      open(i, a);
    });
  });

  dlg.querySelector(".lb-close").addEventListener("click", function () { dlg.close(); });
  dlg.querySelector(".lb-prev").addEventListener("click", function () { show(index - 1); });
  dlg.querySelector(".lb-next").addEventListener("click", function () { show(index + 1); });

  dlg.addEventListener("keydown", function (e) {
    if (e.key === "ArrowLeft") { e.preventDefault(); show(index - 1); }
    else if (e.key === "ArrowRight") { e.preventDefault(); show(index + 1); }
    else if (e.key === "Home") { e.preventDefault(); show(0); }
    else if (e.key === "End") { e.preventDefault(); show(links.length - 1); }
  });

  /* Click on the dark area around the image closes it. */
  var swiped = false;
  dlg.addEventListener("click", function (e) {
    if (swiped) { swiped = false; return; }
    if (e.target === dlg || e.target === stage) dlg.close();
  });

  /* Swipe left or right to move between screenshots. */
  var startX = null, startY = 0;
  stage.addEventListener("pointerdown", function (e) {
    if (e.pointerType === "mouse") return;
    startX = e.clientX; startY = e.clientY;
  });
  stage.addEventListener("pointerup", function (e) {
    if (startX === null) return;
    var dx = e.clientX - startX, dy = e.clientY - startY;
    startX = null;
    if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy)) {
      swiped = true;
      setTimeout(function () { swiped = false; }, 400);
      show(index + (dx < 0 ? 1 : -1));
    }
  });
  stage.addEventListener("pointercancel", function () { startX = null; });
})();
