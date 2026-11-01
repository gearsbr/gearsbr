/**
 * GEARS. — Open Source Environmental Engineering
 * Main Frontend Controller (Navigation, Technical Spec Tabs, Smooth Anchors)
 */

document.addEventListener('DOMContentLoaded', () => {
  /* --------------------------------------------------------------------------
   * 1. Mobile Navigation Toggle
   * -------------------------------------------------------------------------- */
  const mobileMenuBtn = document.getElementById('mobile-menu-toggle');
  const navMenu = document.getElementById('nav-menu');

  if (mobileMenuBtn && navMenu) {
    mobileMenuBtn.addEventListener('click', () => {
      const isExpanded = mobileMenuBtn.getAttribute('aria-expanded') === 'true';
      mobileMenuBtn.setAttribute('aria-expanded', String(!isExpanded));
      navMenu.classList.toggle('open');
    });

    // Close menu when clicking a nav link on mobile
    navMenu.querySelectorAll('.nav-link').forEach((link) => {
      link.addEventListener('click', () => {
        navMenu.classList.remove('open');
        mobileMenuBtn.setAttribute('aria-expanded', 'false');
      });
    });
  }

  /* --------------------------------------------------------------------------
   * 2. T.U.L.I.P.A. Technical Specification Tabs
   * -------------------------------------------------------------------------- */
  const tabButtons = document.querySelectorAll('[data-tech-tab]');
  const tabPanels = document.querySelectorAll('[data-tech-panel]');

  tabButtons.forEach((btn) => {
    btn.addEventListener('click', () => {
      const targetTab = btn.getAttribute('data-tech-tab');

      tabButtons.forEach((b) => {
        b.classList.remove('active');
        b.setAttribute('aria-selected', 'false');
      });
      btn.classList.add('active');
      btn.setAttribute('aria-selected', 'true');

      tabPanels.forEach((panel) => {
        if (panel.getAttribute('data-tech-panel') === targetTab) {
          panel.classList.add('active');
        } else {
          panel.classList.remove('active');
        }
      });
    });
  });

  /* --------------------------------------------------------------------------
   * 3. Active Section Highlighting on Scroll
   * -------------------------------------------------------------------------- */
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-link[href^="#"]');

  const updateActiveNav = () => {
    const scrollY = window.scrollY + 140;
    sections.forEach((sec) => {
      const top = sec.offsetTop;
      const height = sec.offsetHeight;
      const id = sec.getAttribute('id');

      if (scrollY >= top && scrollY < top + height) {
        navLinks.forEach((link) => {
          link.classList.toggle('active', link.getAttribute('href') === `#${id}`);
        });
      }
    });
  };

  window.addEventListener('scroll', updateActiveNav, { passive: true });
  updateActiveNav();
});
