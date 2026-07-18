"use strict";

document.addEventListener("DOMContentLoaded", () => {
    initializeAOS();
    setCurrentYear();
    initializeHeaderState();
    initializeBackToTop();
    initializeActiveNavigation();
    initializeMobileNavigation();
    restrictPhoneInput();
    scrollToInvalidForm();
});

function initializeAOS() {
    if (typeof AOS === "undefined") {
        return;
    }

    const reduceMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    ).matches;

    AOS.init({
        duration: reduceMotion ? 0 : 650,
        easing: "ease-out-cubic",
        once: true,
        offset: 80,
        disable: reduceMotion,
    });
}

function setCurrentYear() {
    const currentYear = new Date().getFullYear();

    document.querySelectorAll("[data-current-year]").forEach((element) => {
        element.textContent = currentYear;
    });
}

function initializeHeaderState() {
    const header = document.querySelector(".site-header");

    if (!header) {
        return;
    }

    const updateHeader = () => {
        header.classList.toggle("is-scrolled", window.scrollY > 12);
    };

    updateHeader();
    window.addEventListener("scroll", updateHeader, { passive: true });
}

function initializeBackToTop() {
    const button = document.querySelector("#backToTop");

    if (!button) {
        return;
    }

    const updateVisibility = () => {
        button.classList.toggle("show", window.scrollY > 500);
    };

    button.addEventListener("click", () => {
        window.scrollTo({ top: 0, behavior: "smooth" });
    });

    updateVisibility();
    window.addEventListener("scroll", updateVisibility, { passive: true });
}

function initializeActiveNavigation() {
    const links = Array.from(
        document.querySelectorAll('.site-navbar .nav-link[href*="#"]')
    );

    const sections = links
        .map((link) => {
            const hash = new URL(link.href, window.location.href).hash;
            return hash ? document.querySelector(hash) : null;
        })
        .filter(Boolean);

    if (!links.length || !sections.length) {
        return;
    }

    const setActiveLink = (sectionId) => {
        links.forEach((link) => {
            const isActive = link.hash === `#${sectionId}`;
            link.classList.toggle("active", isActive);

            if (isActive) {
                link.setAttribute("aria-current", "page");
            } else {
                link.removeAttribute("aria-current");
            }
        });
    };

    const observer = new IntersectionObserver(
        (entries) => {
            const visibleEntry = entries
                .filter((entry) => entry.isIntersecting)
                .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];

            if (visibleEntry) {
                setActiveLink(visibleEntry.target.id);
            }
        },
        {
            rootMargin: "-35% 0px -55% 0px",
            threshold: [0.05, 0.25, 0.5],
        }
    );

    sections.forEach((section) => observer.observe(section));
}

function initializeMobileNavigation() {
    const navigation = document.querySelector("#mainNavigation");

    if (!navigation || typeof bootstrap === "undefined") {
        return;
    }

    navigation.querySelectorAll("a").forEach((link) => {
        link.addEventListener("click", () => {
            if (navigation.classList.contains("show")) {
                bootstrap.Collapse.getOrCreateInstance(navigation).hide();
            }
        });
    });
}

function restrictPhoneInput() {
    const phoneInput = document.querySelector('input[name="phone"]');

    if (!phoneInput) {
        return;
    }

    phoneInput.addEventListener("input", () => {
        phoneInput.value = phoneInput.value.replace(/\D/g, "").slice(0, 10);
    });
}

function scrollToInvalidForm() {
    const formCard = document.querySelector(
        '#enquiry-form[data-has-errors="true"]'
    );

    if (!formCard) {
        return;
    }

    window.requestAnimationFrame(() => {
        formCard.scrollIntoView({ behavior: "smooth", block: "start" });

        const firstInvalidField = formCard.querySelector(".is-invalid");
        firstInvalidField?.focus({ preventScroll: true });
    });
}
