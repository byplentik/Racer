"use strict";

document.addEventListener("DOMContentLoaded", () => {
  const sideNav = document.querySelector(".side-nav");
  
  const updateSideNav = () => {
    sideNav.classList.toggle("fixed");
  };

  window.addEventListener("scroll", updateSideNav);

  updateSideNav();

  const navMobButton = document.querySelector(".nav__mob-button");
  const navMobButtonMobile = document.querySelector(".nav-mob-button");
  const navListWrap = document.querySelector(".nav__list-wrap");

  const toggleAnimateClass = () => {
    navListWrap.classList.toggle("animate");
  };

  const addAnimateClassIfOutsideNavList = (event) => {
    if (!navListWrap.contains(event.target)) {
      navListWrap.classList.add("animate");
    }
  };

  navMobButton.addEventListener("click", toggleAnimateClass);
  navMobButtonMobile.addEventListener("click", toggleAnimateClass);

  document.addEventListener("click", addAnimateClassIfOutsideNavList);
});
