(function () {
  var navwrap = document.getElementById("navwrap");
  var menuBtn = document.querySelector(".menu-btn");
  menuBtn.addEventListener("click", function () {
    var o = navwrap.classList.toggle("open");
    document.querySelector(".top").classList.toggle("menu-open", o);
    document.body.classList.toggle("menu-lock", o);
    menuBtn.setAttribute("aria-expanded", o ? "true" : "false");
  });
  document.querySelectorAll(".sub-toggle").forEach(function (b) {
    b.addEventListener("click", function () {
      var o = b.parentElement.classList.toggle("open");
      b.setAttribute("aria-expanded", o ? "true" : "false");
    });
  });
  document.querySelectorAll("[data-form]").forEach(function (f) {
    var ok = f.querySelector(".form-ok"), err = f.querySelector(".form-err"), btn = f.querySelector("button[type=submit]");
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!f.reportValidity()) return;
      ok.hidden = true; err.hidden = true; btn.disabled = true;
      var data = new FormData(f);
      data.set("name", (data.get("fn") || "") + " " + (data.get("ln") || ""));
      data.set("email", data.get("em") || "");
      fetch(f.action, { method: "POST", body: data, headers: { Accept: "application/json" } })
        .then(function (r) { return r.json(); })
        .then(function (j) { if (!j.success) throw 0; ok.hidden = false; f.reset(); })
        .catch(function () { err.hidden = false; })
        .then(function () { btn.disabled = false; });
    });
  });
})();
