document.addEventListener("DOMContentLoaded", () => {
  AOS.init({
    duration: 750,
    once: true,
    offset: 70,
  });

  const navbar = document.querySelector(".main-navbar");

  const updateStickyNavbar = () => {
    if (!navbar) return;

    if (window.scrollY > 120) {
      navbar.classList.add("sticky-active");
    } else {
      navbar.classList.remove("sticky-active");
    }
  };

  updateStickyNavbar();
  window.addEventListener("scroll", updateStickyNavbar);

  const phoneInput = document.querySelector('input[name="phone"]');
  const pincodeInput = document.querySelector('input[name="pincode"]');

  const allowDigitsOnly = (event) => {
    event.target.value = event.target.value.replace(/\D/g, "");
  };

  phoneInput?.addEventListener("input", allowDigitsOnly);
  pincodeInput?.addEventListener("input", allowDigitsOnly);

  document.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener("click", (event) => {
      const targetId = link.getAttribute("href");

      if (!targetId || targetId === "#") return;

      const target = document.querySelector(targetId);

      if (!target) return;

      event.preventDefault();

      target.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    });
  });
});