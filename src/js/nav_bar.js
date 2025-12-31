// ========================= //
//  Copyright (c) AJ-Holzer  //
//  All rights reserved      //
// ========================= //

const toggle = document.querySelector(".nav-toggle");
const menu = document.querySelector(".nav-menu");
const overlay = document.querySelector(".nav-overlay");

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
