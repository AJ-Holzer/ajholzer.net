// ========================= //
//  Copyright (c) AJ-Holzer  //
//  All rights reserved      //
// ========================= //

document.addEventListener("DOMContentLoaded", () => {
  const username = "AJ-Holzer";
  const container = document.querySelector("#projects-container");

  /* -------------------------
     Cache configuration
  ------------------------- */
  const CACHE_KEY = "github_projects_cache";
  const CACHE_TTL = 24 * 60 * 60 * 1000; // 24 hours

  function shouldBypassCache() {
    const nav = performance.getEntriesByType("navigation")[0];
    const isReload = nav && nav.type === "reload";
    const urlBypass = new URLSearchParams(window.location.search).has(
      "nocache"
    );
    return isReload || urlBypass;
  }

  function getCachedData() {
    try {
      const cached = JSON.parse(localStorage.getItem(CACHE_KEY));
      if (!cached) return null;

      if (Date.now() - cached.timestamp > CACHE_TTL) {
        return null;
      }

      return cached.data;
    } catch {
      return null;
    }
  }

  function setCachedData(data) {
    localStorage.setItem(
      CACHE_KEY,
      JSON.stringify({
        timestamp: Date.now(),
        data,
      })
    );
  }

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
     Data loading (cache aware)
  ------------------------- */
  const bypassCache = shouldBypassCache();
  const cachedData = !bypassCache ? getCachedData() : null;

  if (cachedData) {
    container.innerHTML = "";
    renderHeader();

    cachedData.forEach((repo) => {
      createRow(repo.name, repo.description, repo.commits, repo.url);
    });

    return;
  }

  fetch(
    `https://api.github.com/users/${username}/repos?sort=updated&per_page=5`
  )
    .then((res) => {
      if (!res.ok) throw new Error("GitHub API error");
      return res.json();
    })
    .then(async (repos) => {
      if (!Array.isArray(repos) || repos.length === 0) {
        throw new Error("No repositories");
      }

      container.innerHTML = "";
      renderHeader();

      const result = [];

      for (const repo of repos) {
        if (repo.name === username) continue;

        const row = createRow(
          repo.name,
          repo.description,
          "loading…",
          repo.html_url
        );

        const commits = await fetchCommitCount(username, repo.name, row, true);

        result.push({
          name: repo.name,
          description: repo.description,
          commits,
          url: repo.html_url,
        });
      }

      setCachedData(result);
    })
    .catch(() => {
      renderPlaceholders();
    });
});

/* -------------------------
   Commit count fetcher
------------------------- */
function fetchCommitCount(owner, repo, row, returnCount = false) {
  return fetch(
    `https://api.github.com/repos/${owner}/${repo}/commits?per_page=1`
  )
    .then((res) => {
      const link = res.headers.get("Link");
      if (!link) return 1;

      const match = link.match(/page=(\d+)>; rel="last"/);
      return match ? Number(match[1]) : 1;
    })
    .then((count) => {
      if (row) {
        row.querySelector(".commit-count").textContent = count;
      }
      return returnCount ? count : undefined;
    })
    .catch(() => {
      if (row) {
        row.querySelector(".commit-count").textContent = "—";
      }
      return returnCount ? "—" : undefined;
    });
}
