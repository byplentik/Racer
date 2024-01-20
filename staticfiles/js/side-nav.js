"use strict"

// Get the side nav element
var sideNav = document.querySelector('.side-nav');

// Get the initial offset from the top of the page
var offsetTop = sideNav.offsetTop;

// Function to update the position of the side nav
function updateSideNav() {
  if (window.pageYOffset >= offsetTop) {
    // If the user has scrolled down, fix the side nav
    sideNav.classList.add('fixed');
  } else {
    // If the user is at the top, remove the fixed position
    sideNav.classList.remove('fixed');
  }
}

// Attach the updateSideNav function to the scroll event
window.addEventListener('scroll', updateSideNav);

// Initial call to set the initial state
updateSideNav();


document.addEventListener("DOMContentLoaded", function() {
  var navMobButton = document.querySelector('.nav__mob-button');
  var navMobButtonMobile = document.querySelector('.nav-mob-button');
  var navListWrap = document.querySelector('.nav__list-wrap');

  function toggleAnimateClass() {
    navListWrap.classList.toggle('animate');
  }

  function addAnimateClassIfOutsideNavList(event) {
    var isClickInsideNavList = navListWrap.contains(event.target) || navMobButton.contains(event.target) || navMobButtonMobile.contains(event.target);
    
    if (!isClickInsideNavList) {
      // Clicked outside, add the 'animate' class
      navListWrap.classList.add('animate');
    }
  }

  navMobButton.addEventListener('click', toggleAnimateClass);
  navMobButtonMobile.addEventListener('click', toggleAnimateClass);

  // Add event listener for clicks outside the 'nav__list-wrap'
  document.addEventListener('click', addAnimateClassIfOutsideNavList);
});



