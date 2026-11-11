// =====================================
// 1. MOBILE NAVIGATION
// =====================================
const menuToggle = document.getElementById("menuToggle");
const navLinks = document.getElementById("navLinks");

if (menuToggle && navLinks) {
  menuToggle.addEventListener("click", () => {
    const isOpen = navLinks.classList.toggle("active");
    menuToggle.setAttribute("aria-expanded", isOpen);
    menuToggle.textContent = isOpen ? "✕" : "☰";
  });

  document.querySelectorAll(".nav-links a").forEach((link) => {
    link.addEventListener("click", () => {
      navLinks.classList.remove("active");
      menuToggle.setAttribute("aria-expanded", "false");
      menuToggle.textContent = "☰";
    });
  });
}

// =====================================
// 2. FOOTER YEAR
// =====================================
const yearElement = document.getElementById("year");
if (yearElement) {
  yearElement.textContent = new Date().getFullYear();
}

// =====================================
// 3. FETCH PROJECTS FROM FLASK
// =====================================
async function loadProjects() {
  const projectsGrid = document.getElementById("projectsGrid");
  if (!projectsGrid) return;

  try {
    const response = await fetch("/api/projects");
    if (!response.ok) {
      throw new Error("Unable to fetch projects");
    }

    const projects = await response.json();
    projectsGrid.innerHTML = "";

    if (projects.length === 0) {
      projectsGrid.textContent = "No projects available.";
      return;
    }

    projects.forEach((project) => {
      const card = document.createElement("article");
      card.className = "project-card";

      const tags = project.tech_stack
        .split(",")
        .map((tech) => `<span>${escapeHTML(tech.trim())}</span>`)
        .join("");

      const githubLink = project.github_url
        ? `<a href="${safeURL(project.github_url)}" target="_blank" rel="noopener noreferrer" class="project-link">GitHub ↗</a>`
        : "";

      const demoLink = project.demo_url
        ? `<a href="${safeURL(project.demo_url)}" target="_blank" rel="noopener noreferrer" class="project-link">Live Demo ↗</a>`
        : "";

      card.innerHTML = `
        <div class="project-number">PROJECT ${String(project.id).padStart(2, "0")}</div>
        <div class="project-icon">💻</div>
        <h3>${escapeHTML(project.title)}</h3>
        <p>${escapeHTML(project.description)}</p>
        <div class="project-tags">
          ${tags}
        </div>
        <div class="project-actions">
          ${githubLink}
          ${demoLink}
        </div>
      `;

      projectsGrid.appendChild(card);
    });
  } catch (error) {
    console.error("Project loading error:", error);
    projectsGrid.textContent =
      "Unable to load projects. Please try again later.";
  }
}

// =====================================
// 4. FETCH SKILLS FROM FLASK
// =====================================
async function loadSkills() {
  const skillsGrid = document.getElementById("skillsGrid");
  if (!skillsGrid) return;

  try {
    const response = await fetch("/api/skills");
    if (!response.ok) {
      throw new Error("Unable to fetch skills");
    }

    const skills = await response.json();
    skillsGrid.innerHTML = "";

    if (skills.length === 0) {
      skillsGrid.textContent = "No skills available.";
      return;
    }

    // Group skills by category
    const groupedSkills = {};
    skills.forEach((skill) => {
      if (!groupedSkills[skill.category]) {
        groupedSkills[skill.category] = [];
      }
      groupedSkills[skill.category].push(skill.name);
    });

    Object.entries(groupedSkills).forEach(([category, names], index) => {
      const card = document.createElement("div");
      card.className = "skill-card";
      card.innerHTML = `
        <span>${String(index + 1).padStart(2, "0")}</span>
        <h3>${escapeHTML(category)}</h3>
        <div class="skill-tags">
          ${names.map((name) => `<span>${escapeHTML(name)}</span>`).join("")}
        </div>
      `;
      skillsGrid.appendChild(card);
    });
  } catch (error) {
    console.error("Skills loading error:", error);
    skillsGrid.textContent = "Unable to load skills. Please try again later.";
  }
}

// =====================================
// 5. SAFE TEXT AND URL HANDLING
// =====================================
function escapeHTML(value) {
  return String(value).replace(
    /[&<>"']/g,
    (character) =>
      ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;",
      })[character]
  );
}

function safeURL(value) {
  try {
    const url = new URL(value);
    if (url.protocol === "https:" || url.protocol === "http:") {
      return url.href;
    }
  } catch (error) {
    console.warn("Invalid project URL:", value);
  }
  return "#";
}

// =====================================
// 6. INITIALIZE PORTFOLIO
// =====================================
document.addEventListener("DOMContentLoaded", () => {
  loadProjects();
  loadSkills();
  console.log("Portfolio frontend initialized.");
});
