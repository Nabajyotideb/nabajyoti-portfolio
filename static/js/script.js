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


// =====================================
// 7. CONTACT FORM INTEGRATION
// =====================================
const contactForm = document.getElementById("contactForm");
const formStatus = document.getElementById("formStatus");
const submitBtn = document.getElementById("submitBtn");

if (contactForm && formStatus && submitBtn) {
  contactForm.addEventListener("submit", async (event) => {
    // Prevent normal page reload
    event.preventDefault();

    // Get values from form
    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const message = document.getElementById("message").value.trim();

    // Frontend validation
    if (!name || !email || !message) {
      formStatus.textContent = "Please fill in all fields.";
      formStatus.className = "form-status error";
      return;
    }

    // Disable button while sending
    submitBtn.disabled = true;
    submitBtn.textContent = "Sending...";
    formStatus.textContent = "";
    formStatus.className = "form-status";

    try {
      // Send data to Flask backend
      const response = await fetch("/api/messages", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: name,
          email: email,
          message: message,
        }),
      });

      const result = await response.json();

      if (!response.ok) {
        throw new Error(
          result.message || result.error || "Unable to send message."
        );
      }

      // Display success notification
      if (result.notification_sent) {
        formStatus.textContent =
          "Message sent successfully! I'll get back to you soon.";
      } else {
        formStatus.textContent =
          "Message saved successfully, but email notification could not be sent.";
      }
      formStatus.className = "form-status success";

      // Clear form after successful submission
      contactForm.reset();
    } catch (error) {
      console.error("Contact form error:", error);
      formStatus.textContent =
        error.message || "Something went wrong. Please try again.";
      formStatus.className = "form-status error";
    } finally {
      // Enable button again
      submitBtn.disabled = false;
      submitBtn.textContent = "Send Message ↗";
    }
  });
}
