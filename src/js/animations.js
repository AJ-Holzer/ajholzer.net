// ========================= //
//  Copyright (c) AJ-Holzer  //
//  All rights reserved      //
// ========================= //

window.addEventListener("DOMContentLoaded", () => {
  const revealElements = document.querySelectorAll(".reveal");

  const observer = new IntersectionObserver(
    (entries, obs) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const el = entry.target;

          // Apply staggered delay only when revealed
          const index = [...revealElements].indexOf(el);
          el.style.animationDelay = `${index * 0.1}s`;

          el.classList.add("is-visible");
          obs.unobserve(el); // animate once
        }
      });
    },
    {
      threshold: 0.1,
    }
  );

  revealElements.forEach((el) => observer.observe(el));
});
