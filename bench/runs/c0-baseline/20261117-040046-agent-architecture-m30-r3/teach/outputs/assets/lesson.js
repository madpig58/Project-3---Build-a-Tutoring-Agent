// Practice checks: mark the chosen option and explain it at once.
document.querySelectorAll("[data-check]").forEach(function (box) {
  var buttons = box.querySelectorAll("button[data-correct]");
  var out = box.querySelector(".feedback");
  buttons.forEach(function (button) {
    button.addEventListener("click", function () {
      buttons.forEach(function (b) { b.classList.remove("right", "wrong"); });
      var right = button.getAttribute("data-correct") === "true";
      button.classList.add(right ? "right" : "wrong");
      if (out) { out.textContent = (right ? "Yes. " : "Not quite. ") + (button.getAttribute("data-why") || ""); }
    });
  });
});
