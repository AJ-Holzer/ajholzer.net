// ========================= //
//  Copyright (c) AJ-Holzer  //
//  All rights reserved      //
// ========================= //

document.addEventListener("DOMContentLoaded", () => {
  const container = document.querySelector("#projects-container");
  const API_URL = "https://api.ajholzer.net/github/projects";

  /* -------------------------
     Reveal system
  ------------------------- */
  const revealObserver = new IntersectionObserver(
    (entries, obs) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          obs.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1 }
  );

  function observeReveal(el) {
    el.classList.add("reveal");
    revealObserver.observe(el);
  }

  /* -------------------------
     Header row
  ------------------------- */
  function renderHeader() {
    const header = document.createElement("div");
    header.className = "project project-header";
    header.innerHTML = `
      <div>Project</div>
      <div>Description</div>
      <div class="project-commit-header">Commits</div>
    `;
    container.appendChild(header);
    observeReveal(header);
  }

  /* -------------------------
     Placeholder projects
  ------------------------- */
  const PLACEHOLDERS = [
    {
      name: "Debbie",
      description: "Quadrupedal robot with encrypted WiFi control.",
    },
    {
      name: "CHATLEX",
      description: "Secure messaging application with local encryption.",
    },
  ];

  function createRow(name, description, commits = "—", url = "#") {
    const row = document.createElement("div");

    row.innerHTML = `
      <a class="project" href="${url}" target="_blank" rel="noopener noreferrer">
        <div class="project-title">${name}</div>
        <div class="project-description">
          ${description || "No description available."}
        </div>
        <div class="project-commit-count">${commits}</div>
      </a>
    `;

    container.appendChild(row);
    observeReveal(row);
  }

  function renderPlaceholders() {
    container.innerHTML = "";
    renderHeader();
    PLACEHOLDERS.forEach((p) => createRow(p.name, p.description, "—"));
  }

  /* -------------------------
     Initial state
  ------------------------- */
  renderPlaceholders();

  /* -------------------------
     Data loading (API only)
  ------------------------- */
  fetch(API_URL)
    .then((res) => {
      if (!res.ok) throw new Error("API error");
      return res.json();
    })
    .then((projects) => {
      if (!Array.isArray(projects) || projects.length === 0) {
        throw new Error("No projects");
      }

      container.innerHTML = "";
      renderHeader();

      projects.forEach((project) => {
        createRow(
          project.name,
          project.description,
          project.commit_count ?? "—",
          project.url
        );
      });
    })
    .catch(() => {
      renderPlaceholders();
    });
});
