// ========================= //
//  Copyright (c) AJ-Holzer  //
//  All rights reserved      //
// ========================= //

// Get elements by id
const toggle = document.querySelector(".nav-toggle");
const menu = document.querySelector(".nav-menu");
const overlay = document.querySelector(".nav-overlay");

// Select all links inside the nav menu
const navLinks = document.querySelectorAll(".nav-menu a");

// Add click listener to each link
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
