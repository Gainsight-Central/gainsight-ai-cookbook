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

  // Download gate for the CSM Adoption Agent plugin. Nothing is sent to Google
  // until the form is submitted. Other kits keep their plain download links.
  var GATE = {
    form: "https://docs.google.com/forms/d/e/1FAIpQLSd2YwT7aUZNbzA5MGDE5gR5OLmirrneQp-VH1v20aC5UOaVug/formResponse",
    fields: {
      name: "entry.1235685806",
      email: "entry.1051090612",
      company: "entry.650553045",
      role: "entry.1466077044",
      use: "entry.1437994415"
    }
  };

  var dialog = document.getElementById("nba-gate");
  var gateForm = document.getElementById("nba-gate-form");
  var gateLink = document.querySelector("[data-gate='nba']");

  function startDownload(href) {
    var a = document.createElement("a");
    a.href = href;
    a.download = "";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  }

  if (dialog && gateForm && gateLink && typeof dialog.showModal === "function") {
    var href = gateLink.getAttribute("href");
    var submitBtn = gateForm.querySelector("[type='submit']");
    var sending = false;

    gateLink.addEventListener("click", function (event) {
      event.preventDefault();
      sending = false;
      submitBtn.disabled = false;
      cancelBtn.disabled = false;
      submitBtn.textContent = "Download";
      if (!dialog.open) dialog.showModal();
    });

    // Enter in a text field moves to the next field. It only submits from the Download button,
    // so people do not skip the optional Role and usage fields by accident.
    var fieldOrder = Array.prototype.slice.call(gateForm.querySelectorAll("input, textarea"));
    // A required field with only spaces counts as empty.
    function checkBlank(field) {
      if (field.required && field.type === "text" && !field.value.trim()) {
        field.setCustomValidity("Please fill out this field.");
      } else {
        field.setCustomValidity("");
      }
    }

    fieldOrder.forEach(function (field, i) {
      field.addEventListener("input", function () { checkBlank(field); });
      field.addEventListener("keydown", function (event) {
        if (event.key !== "Enter" || event.isComposing) return;
        event.preventDefault();
        checkBlank(field);
        // Stay on a required or invalid field and show the error. Optional empty fields move on.
        if (!field.checkValidity()) {
          field.reportValidity();
          return;
        }
        var next = fieldOrder[i + 1];
        if (next) {
          next.focus();
        } else if (gateForm.requestSubmit) {
          // Last field. Enter submits, and the required fields are checked again.
          gateForm.requestSubmit(submitBtn);
        } else {
          submitBtn.click();
        }
      });
    });

    var cancelBtn = dialog.querySelector("[data-gate-close]");
    cancelBtn.addEventListener("click", function () {
      if (!sending) dialog.close();
    });

    // Esc fires "cancel" on a dialog. Ignore it while the download is starting.
    dialog.addEventListener("cancel", function (event) {
      if (sending) event.preventDefault();
    });

    gateForm.addEventListener("submit", function (event) {
      event.preventDefault();
      if (sending) return;
      sending = true;
      submitBtn.disabled = true;
      cancelBtn.disabled = true;
      submitBtn.textContent = "Starting download...";
      var data = new FormData();
      data.append(GATE.fields.name, gateForm.elements.name.value.trim());
      data.append(GATE.fields.email, gateForm.elements.email.value.trim());
      data.append(GATE.fields.company, gateForm.elements.company.value.trim());
      var role = gateForm.elements.role.value.trim();
      var use = gateForm.elements.use.value.trim();
      if (role) data.append(GATE.fields.role, role);
      if (use) data.append(GATE.fields.use, use);
      // no-cors hides the response, so the download starts even if the post fails.
      // Wait at most 3 seconds for Google, so a slow post never blocks the download.
      Promise.race([
        fetch(GATE.form, { method: "POST", mode: "no-cors", body: data }).catch(function () {}),
        new Promise(function (resolve) { window.setTimeout(resolve, 3000); })
      ])
        .then(function () {
          dialog.close();
          startDownload(href);
        });
    });
  }
})();
