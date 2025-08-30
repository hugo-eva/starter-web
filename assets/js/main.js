// Lumy TV - global JS: nav, GA, lazy images, calculator
(function () {
  // Theme: respect system and persist user choice
  (function initTheme() {
    try {
      const stored = localStorage.getItem('theme');
      const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
      const theme = stored || (prefersDark ? 'dark' : 'light');
      if (theme === 'dark') document.documentElement.classList.add('dark');
    } catch (_) {}
  })();
  window.dataLayer = window.dataLayer || [];
  function gtag(){ dataLayer.push(arguments); }
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');

  document.addEventListener('click', function (e) {
    const a = e.target.closest('a[href^="#"]');
    if (!a) return;
    const id = a.getAttribute('href').slice(1);
    const el = document.getElementById(id);
    if (el) {
      e.preventDefault();
      el.scrollIntoView({ behavior: 'smooth' });
    }
  });

  const lazyImages = Array.from(document.querySelectorAll('img[loading="lazy"][data-src]'));
  if ('IntersectionObserver' in window && lazyImages.length) {
    const io = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src;
          img.removeAttribute('data-src');
          obs.unobserve(img);
        }
      });
    }, { rootMargin: '200px' });
    lazyImages.forEach(img => io.observe(img));
  } else {
    lazyImages.forEach(img => { img.src = img.dataset.src; img.removeAttribute('data-src'); });
  }

  function formatEUR(value) { 
    const locale = window.i18n && window.i18n.currentLanguage === 'en' ? 'en-US' : 'pt-PT';
    return new Intl.NumberFormat(locale, { style: 'currency', currency: 'EUR' }).format(value); 
  }
  function calculatePrice({ screens, storageGb, annual }) {
    const base = 9; const storagePerGb = 0.5; const monthly = screens * base + storageGb * storagePerGb;
    return annual ? monthly * 12 * 0.8 : monthly;
  }
  function initPricing() {
    const calcRoots = Array.from(document.querySelectorAll('[data-calc-root]'));
    if (!calcRoots.length) return;

    let annual = false;
    const toggleButtons = Array.from(document.querySelectorAll('[data-billing]'));

    function updateCalc(el) {
      const screens = el.querySelector('[name="screens"]');
      const storage = el.querySelector('[name="storage"]');
      const output = el.querySelector('[data-price-output]');
      if (!screens || !storage || !output) return;
      const price = calculatePrice({ screens: Number(screens.value), storageGb: Number(storage.value), annual });
      const isEnglish = document.documentElement.lang === 'en';
      output.textContent = annual ? formatEUR(price) + (isEnglish ? ' / year' : ' / ano') : formatEUR(price) + (isEnglish ? ' / month' : ' / mês');
    }

    function updateAll() { calcRoots.forEach(updateCalc); }

    // Global toggle controls
    toggleButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        toggleButtons.forEach(b => b.setAttribute('aria-pressed', 'false'));
        btn.setAttribute('aria-pressed', 'true');
        annual = btn.dataset.billing === 'annual';
        updateAll();
      });
    });

    // Inputs within calculators
    calcRoots.forEach(el => {
      const screens = el.querySelector('[name="screens"]');
      const storage = el.querySelector('[name="storage"]');
      if (screens) screens.addEventListener('input', updateAll);
      if (storage) storage.addEventListener('input', updateAll);
    });

    // Initialize default pressed state if present
    const pressed = toggleButtons.find(b => b.getAttribute('aria-pressed') === 'true');
    annual = pressed ? pressed.dataset.billing === 'annual' : false;
    updateAll();
  }
  document.addEventListener('DOMContentLoaded', function () {
    initPricing();

    // Theme toggle handler (supports multiple buttons)
    const toggles = Array.from(document.querySelectorAll('[data-theme-toggle]'));
    if (toggles.length) {
      function updateLabels() {
        const isDark = document.documentElement.classList.contains('dark');
        const isEnglish = document.documentElement.lang === 'en';
        toggles.forEach(t => {
          t.setAttribute('aria-pressed', String(isDark));
          if (isEnglish) {
            t.textContent = isDark ? 'Light mode' : 'Dark mode';
          } else {
            t.textContent = isDark ? 'Modo claro' : 'Modo escuro';
          }
        });
      }
      toggles.forEach(t => t.addEventListener('click', function () {
        const isDark = document.documentElement.classList.toggle('dark');
        try { localStorage.setItem('theme', isDark ? 'dark' : 'light'); } catch (_) {}
        updateLabels();
      }));
      updateLabels();
    }

    // Mobile nav toggle
    const header = document.querySelector('.site-header');
    const navToggle = document.querySelector('[data-nav-toggle]');
    const mobileMenu = document.getElementById('mobile-menu');
    function setMenuOpen(isOpen) {
      if (!header || !navToggle || !mobileMenu) return;
      header.classList.toggle('open', isOpen);
      navToggle.setAttribute('aria-expanded', String(isOpen));
      mobileMenu.hidden = !isOpen;
    }
    if (header && navToggle && mobileMenu) {
      navToggle.addEventListener('click', function () {
        const isOpen = !header.classList.contains('open');
        setMenuOpen(isOpen);
      });
      mobileMenu.addEventListener('click', function (e) {
        const link = e.target && e.target.closest && e.target.closest('a');
        if (link) setMenuOpen(false);
      });
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') setMenuOpen(false);
      });
      const mq = window.matchMedia('(min-width: 860px)');
      if (mq && mq.addEventListener) {
        mq.addEventListener('change', (e) => { if (e.matches) setMenuOpen(false); });
      }
      // Ensure hidden on load
      setMenuOpen(false);
    }
  });
})();

