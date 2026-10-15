(function () {
  function sourceText(id) {
    var el = document.getElementById(id);
    if (!el) return "";
    return el.textContent.replace(/^\n/, "").replace(/\n$/, "");
  }

  function markCopied(btn) {
    var previous = btn.getAttribute("data-label") || btn.textContent;
    btn.setAttribute("data-label", previous);
    btn.textContent = "Copied";
    window.setTimeout(function () {
      btn.textContent = previous;
    }, 1600);
  }

  function fallback(text) {
    var area = document.createElement("textarea");
    area.value = text;
    area.setAttribute("readonly", "");
    area.style.position = "fixed";
    area.style.left = "-9999px";
    document.body.appendChild(area);
    area.select();
    try {
      document.execCommand("copy");
    } catch (error) {
      return;
    }
    document.body.removeChild(area);
  }

  document.querySelectorAll("[data-copy]").forEach(function (btn) {
    btn.addEventListener("click", function (event) {
      event.preventDefault();
      var text = sourceText(btn.getAttribute("data-copy"));
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(
          function () { markCopied(btn); },
          function () { fallback(text); markCopied(btn); }
        );
      } else {
        fallback(text);
        markCopied(btn);
      }
    });
  });
})();
