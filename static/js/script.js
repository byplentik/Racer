"use strict";

const toTopButton = document.getElementById("to-top");

if (toTopButton) {
  toTopButton.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  window.addEventListener("scroll", () => {
    if (
      document.body.scrollTop > 1270 ||
      document.documentElement.scrollTop > 1270
    ) {
      toTopButton.style.display = "block";
    } else {
      toTopButton.style.display = "none";
    }
  });

  const links = document.querySelectorAll('a[href^="#r"]');

  links?.forEach((link) => {
    link.addEventListener("click", (event) => {
      event.preventDefault();
      const targetId = this.getAttribute("href").substring(1);

      const targetElement = document.getElementById(targetId);

      if (targetElement) {
        targetElement.scrollIntoView({ behavior: "smooth" });
      }
    });
  });
}
