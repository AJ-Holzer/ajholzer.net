// ========================= //
//  Copyright (c) AJ-Holzer  //
//  All rights reserved      //
// ========================= //

// Get elements
const toggle = document.querySelector(".nav-toggle");
const menu = document.querySelector(".nav-menu");
const overlay = document.querySelector(".nav-overlay");
const navbar = document.querySelector(".navbar");

// Select all links inside the nav menu
const navLinks = document.querySelectorAll(".nav-menu a");

// --------------------------
// Menu toggle + link clicks
// --------------------------
navLinks.forEach((link) => {
  link.addEventListener("click", () => {
    closeMenu();
  });
});

toggle.addEventListener("click", () => {
  toggle.classList.toggle("open");
  menu.classList.toggle("open");
  overlay.classList.toggle("open");
});

overlay.addEventListener("click", closeMenu);

function closeMenu() {
  toggle.classList.remove("open");
  menu.classList.remove("open");
  overlay.classList.remove("open");
}

// --------------------------
// Hide-on-scroll navbar
// --------------------------
let lastScroll = 0;

// Get the CSS variable value for navbar height in rem
let navbarHeightRem =
  getComputedStyle(document.documentElement).getPropertyValue(
    "--navbar-height"
  ) || "5rem"; // fallback

// Convert rem to pixels
const rootFontSize = parseFloat(
  getComputedStyle(document.documentElement).fontSize
); // usually 16px
const navbarHeightPx = parseFloat(navbarHeightRem) * rootFontSize;

window.addEventListener("scroll", () => {
  const currentScroll = window.scrollY;

  if (currentScroll <= 0) {
    // At the very top → show navbar
    navbar.style.top = "0";
  } else if (currentScroll > lastScroll) {
    // Scrolling down → hide navbar
    navbar.style.top = `-${navbarHeightPx}px`;
  } else {
    // Scrolling up → show navbar
    navbar.style.top = "0";
  }

  lastScroll = currentScroll;
});
