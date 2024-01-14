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
