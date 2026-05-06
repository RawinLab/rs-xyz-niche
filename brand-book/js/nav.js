/* ============================================================
   NICHE Brand Book — Navigation & UI
   Vanilla JS — no build step, no dependencies
   ============================================================ */

(function () {
  'use strict';

  /* ----------------------------------------------------------
     Reading progress bar
     ---------------------------------------------------------- */
  const progressBar = document.querySelector('.reading-progress__bar');
  if (progressBar) {
    function updateProgress() {
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      const scrolled  = window.scrollY;
      const pct       = docHeight > 0 ? (scrolled / docHeight) * 100 : 0;
      progressBar.style.width = pct.toFixed(1) + '%';
    }
    window.addEventListener('scroll', updateProgress, { passive: true });
    updateProgress();
  }

  /* ----------------------------------------------------------
     Sidebar active section highlighting
     ---------------------------------------------------------- */
  const sidebarLinks = document.querySelectorAll('.book-sidebar__toc a');
  if (sidebarLinks.length > 0) {
    const headings = Array.from(
      document.querySelectorAll('h2[id], h3[id]')
    );

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const id = entry.target.getAttribute('id');
            sidebarLinks.forEach((link) => {
              link.classList.toggle(
                'active',
                link.getAttribute('href') === '#' + id
              );
            });
          }
        });
      },
      { rootMargin: '-20% 0px -70% 0px' }
    );

    headings.forEach((h) => observer.observe(h));
  }

  /* ----------------------------------------------------------
     Cover hero word-by-word reveal
     ---------------------------------------------------------- */
  const coverTitle = document.querySelector('.cover-hero__title');
  if (coverTitle) {
    const inners = coverTitle.querySelectorAll('.word-inner');
    inners.forEach((el, i) => {
      const delay = i * 80; // 80ms stagger per word
      setTimeout(() => {
        el.classList.add('revealed');
      }, 200 + delay);
    });
  }

  /* ----------------------------------------------------------
     Motion bar animation on scroll into view
     ---------------------------------------------------------- */
  const motionBars = document.querySelectorAll('.motion-bar-fill');
  if (motionBars.length > 0) {
    const barObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('animate');
            barObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.5 }
    );
    motionBars.forEach((bar) => barObserver.observe(bar));
  }

  /* ----------------------------------------------------------
     Scroll-reveal for section blocks
     ---------------------------------------------------------- */
  const revealEls = document.querySelectorAll('.reveal-on-scroll');
  if (revealEls.length > 0 && window.matchMedia('(prefers-reduced-motion: no-preference)').matches) {
    const revealObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            revealObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1, rootMargin: '0px 0px -60px 0px' }
    );
    revealEls.forEach((el) => revealObserver.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add('is-visible'));
  }

  /* ----------------------------------------------------------
     Smooth scroll for in-page anchor links
     ---------------------------------------------------------- */
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        const offset = 72; // account for fixed topbar
        const top = target.getBoundingClientRect().top + window.scrollY - offset;
        window.scrollTo({ top, behavior: 'smooth' });
      }
    });
  });

  /* ----------------------------------------------------------
     Mobile sidebar toggle
     ---------------------------------------------------------- */
  const sidebarToggle = document.querySelector('.sidebar-toggle');
  const sidebar       = document.querySelector('.book-sidebar');
  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener('click', () => {
      sidebar.classList.toggle('is-open');
      sidebarToggle.setAttribute(
        'aria-expanded',
        sidebar.classList.contains('is-open') ? 'true' : 'false'
      );
    });
  }

  /* ----------------------------------------------------------
     Copy hex value on swatch click
     ---------------------------------------------------------- */
  document.querySelectorAll('.swatch__hex').forEach((el) => {
    el.style.cursor = 'pointer';
    el.title = 'Click to copy';
    el.addEventListener('click', () => {
      const hex = el.textContent.trim();
      if (navigator.clipboard) {
        navigator.clipboard.writeText(hex).then(() => {
          const orig = el.textContent;
          el.textContent = 'Copied!';
          setTimeout(() => { el.textContent = orig; }, 1200);
        });
      }
    });
  });

})();
