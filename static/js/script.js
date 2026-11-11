// ==============================
// 1. MOBILE NAVIGATION
// ==============================
const menuToggle = document.getElementById("menuToggle");
const navLinks = document.getElementById("navLinks");

if (menuToggle && navLinks) {
  menuToggle.addEventListener("click", () => {
    const isOpen = navLinks.classList.toggle("active");
    menuToggle.setAttribute("aria-expanded", isOpen);
    menuToggle.textContent = isOpen ? "✕" : "☰";
  });

  // Close menu after clicking a navigation link
  document.querySelectorAll(".nav-links a").forEach((link) => {
    link.addEventListener("click", () => {
      navLinks.classList.remove("active");
      menuToggle.setAttribute("aria-expanded", "false");
      menuToggle.textContent = "☰";
    });
  });
}

// ==============================
// 2. AUTOMATIC FOOTER YEAR
// ==============================
const yearElement = document.getElementById("year");
if (yearElement) {
  yearElement.textContent = new Date().getFullYear();
}

// ==============================
// 3. CONSOLE MESSAGE
// ==============================
console.log("Welcome to Nabajyoti's Portfolio!");
console.log("Portfolio frontend loaded successfully.");
