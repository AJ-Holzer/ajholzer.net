// ========================= //
//  Copyright (c) AJ-Holzer  //
//  All rights reserved      //
// ========================= //

document.addEventListener("DOMContentLoaded", () => {
  const username = "AJ-Holzer";
  const container = document.querySelector("#projects-container");

  /* -------------------------
     Header row
  ------------------------- */
  function renderHeader() {
    const header = document.createElement("div");
    header.className = "project header";
    header.innerHTML = `
      <div>Project</div>
      <div>Description</div>
      <div class="commit-header">Commits</div>
    `;
    container.appendChild(header);
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
      name: "Chatlex",
      description: "Secure messaging application with local encryption.",
    },
  ];

  function createRow(name, description, commits = "—", url = "#") {
    const row = document.createElement("a");
    row.className = "project";
    row.href = url;
    row.target = "_blank";
    row.rel = "noopener noreferrer";

    row.innerHTML = `
    <div class="title">${name}</div>
    <div class="description">
      ${description || "No description available."}
    </div>
    <div class="commit-count">${commits}</div>
  `;

    container.appendChild(row);
    return row;
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
     Fetch GitHub repositories
  ------------------------- */
  fetch(
    `https://api.github.com/users/${username}/repos?sort=updated&per_page=5`
  )
    .then((res) => {
      if (!res.ok) throw new Error("GitHub API error");
      return res.json();
    })
    .then((repos) => {
      if (!Array.isArray(repos) || repos.length === 0) {
        throw new Error("No repositories");
      }

      container.innerHTML = "";
      renderHeader();

      repos.forEach((repo) => {
        if (repo.name === username) return;

        const row = createRow(
          repo.name,
          repo.description,
          "loading…",
          repo.html_url
        );

        fetchCommitCount(username, repo.name, row);
      });
    })
    .catch(() => {
      renderPlaceholders();
    });
});

/* -------------------------
   Commit count fetcher
------------------------- */
function fetchCommitCount(owner, repo, row) {
  fetch(`https://api.github.com/repos/${owner}/${repo}/commits?per_page=1`)
    .then((res) => {
      const link = res.headers.get("Link");
      if (!link) return 1;

      const match = link.match(/page=(\d+)>; rel="last"/);
      return match ? Number(match[1]) : 1;
    })
    .then((count) => {
      row.querySelector(".commit-count").textContent = count;
    })
    .catch(() => {
      row.querySelector(".commit-count").textContent = "—";
    });
}
