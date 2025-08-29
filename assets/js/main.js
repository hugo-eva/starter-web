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
  function initCalculator() {
    const el = document.querySelector('[data-calc-root]');
    if (!el) return;
    const screens = el.querySelector('[name="screens"]');
    const storage = el.querySelector('[name="storage"]');
    const billingButtons = Array.from(el.querySelectorAll('[data-billing]'));
    const output = el.querySelector('[data-price-output]');
    let annual = false;
    function update() {
      const price = calculatePrice({ screens: Number(screens.value), storageGb: Number(storage.value), annual });
      output.textContent = annual ? formatEUR(price) + ' / ano' : formatEUR(price) + ' / mês';
    }
    billingButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        billingButtons.forEach(b => b.setAttribute('aria-pressed', 'false'));
        btn.setAttribute('aria-pressed', 'true');
        annual = btn.dataset.billing === 'annual';
        update();
      });
    });
    screens.addEventListener('input', update);
    storage.addEventListener('input', update);
    update();
  }
  document.addEventListener('DOMContentLoaded', initCalculator);
})();

