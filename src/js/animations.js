// ========================= //
//  Copyright (c) AJ-Holzer  //
//  All rights reserved      //
// ========================= //

window.addEventListener("DOMContentLoaded", () => {
  const revealElements = document.querySelectorAll(".reveal");

  revealElements.forEach((el, index) => {
    el.style.animationDelay = `${index * 0.1}s`;
  });
});
