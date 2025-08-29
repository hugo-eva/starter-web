// Lumy TV - global JS: nav, GA, lazy images, calculator
(function () {
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

  function formatEUR(value) { return new Intl.NumberFormat('pt-PT', { style: 'currency', currency: 'EUR' }).format(value); }
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
      output.textContent = annual ? formatEUR(price) + ' / ano' : formatEUR(price) + ' / mês';
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
  document.addEventListener('DOMContentLoaded', initPricing);
})();

