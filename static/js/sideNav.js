"use strict";

const navMobButton = document.querySelector(".nav__mob-button");
const navMobButtonMobile = document.querySelector(".nav-mob-button");
const navListWrap = document.querySelector(".nav__list-wrap");

const toggleAnimateClass = () => {
  navListWrap.classList.toggle("animate");
};

const addAnimateClassIfOutsideNavList = (event) => {
  const isClickInsideNavList =
    navListWrap.contains(event.target) ||
    navMobButton.contains(event.target) ||
    navMobButtonMobile.contains(event.target);

  if (!isClickInsideNavList) {
    navListWrap.classList.add("animate");
  }
};

navMobButton.addEventListener("click", toggleAnimateClass);
navMobButtonMobile.addEventListener("click", toggleAnimateClass);

document.addEventListener("click", addAnimateClassIfOutsideNavList);