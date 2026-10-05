(() => {
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Pantalla de arranque con loader (en cada carga) */
  const boot = $('#boot');
  if (reduce) boot.remove();
  else {
    const msgs = ['Cargando portafolio...', 'Compilando proyectos...', 'Bienvenido'];
    const bar = $('#boot-bar i'), txt = $('#boot-text');
    let loaded = document.readyState === 'complete', done = false;
    addEventListener('load', () => (loaded = true));
    const t0 = performance.now();
    const finish = () => {
      if (done) return;
      done = true;
      clearInterval(iv);
      bar.style.width = '100%';
      setTimeout(() => { boot.classList.add('off'); setTimeout(() => boot.remove(), 600); }, 250);
    };
    const iv = setInterval(() => {
      const p = Math.min((performance.now() - t0) / 1800 * 100, loaded ? 100 : 90);
      bar.style.width = p + '%';
      txt.textContent = msgs[Math.min(Math.floor(p / 34), msgs.length - 1)];
      if (p >= 100) finish();
    }, 60);
    setTimeout(6000);
  }

  /* Menú móvil */
  const burger = $('.burger'), menu = $('#menu');
  burger.addEventListener('click', () => burger.setAttribute('aria-expanded', menu.classList.toggle('open')));
  menu.addEventListener('click', e => {
    if (e.target.tagName === 'A') { menu.classList.remove('open'); burger.setAttribute('aria-expanded', 'false'); }
  });

  /* Texto que se escribe */
  const roles = ['Desarrollo de software', 'Backend con Node.js y TypeScript', 'Datos y automatización'];
  const typed = $('#typed');
  let r = 0, c = 0, del = false;
  const type = () => {
    const w = roles[r];
    typed.textContent = w.slice(0, c);
    if (!del && c === w.length) { del = true; return setTimeout(type, 1600); }
    if (del && c === 0) { del = false; r = (r + 1) % roles.length; }
    c += del ? -1 : 1;
    setTimeout(type, del ? 35 : 70);
  };
  reduce ? (typed.textContent = roles[0]) : type();

  /* Contadores: "tools" y "projects" se calculan del HTML */
  const target = el => {
    const v = el.dataset.count;
    if (v === 'tools') return $$('.tool').length;
    if (v === 'projects') return $$('.project:not(.empty)').length;
    return +v;
  };
  const count = el => {
    const end = target(el), suf = el.dataset.suf || '';
    if (reduce) return (el.textContent = end + suf);
    const t0 = performance.now();
    const step = t => {
      const p = Math.min((t - t0) / 1200, 1);
      el.textContent = Math.round(end * p) + (p === 1 ? suf : '');
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };
  $$('.stats b').forEach(b => setTimeout(() => count(b), reduce ? 200 : 2300));

  /* Aparición al hacer scroll */
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
  }), { threshold: 0.12 });
  $$('.reveal').forEach(sec => {
    $$('h2, .lead, .mini, .project, .cert, .tool, .contact > *', sec).forEach((el, i) => {
      el.classList.add('rv');
      el.style.setProperty('--d', Math.min(i * 0.08, 0.7) + 's');
    });
    io.observe(sec);
  });

  /* Carrusel horizontal */
  const track = $('.track');
  $$('.nav-btn').forEach(b => b.addEventListener('click', () => {
    const d = +b.dataset.dir, max = track.scrollWidth - track.clientWidth - 4;
    const behavior = reduce ? 'auto' : 'smooth';
    if (d > 0 && track.scrollLeft >= max) track.scrollTo({ left: 0, behavior });
    else if (d < 0 && track.scrollLeft <= 4) track.scrollTo({ left: max, behavior });
    else track.scrollBy({ left: d * 260, behavior });
  }));

  /* Imágenes de proyecto: si falta el archivo, muestra un marcador */
  const ph = ini => 'data:image/svg+xml,' + encodeURIComponent(
    `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 180"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2a1b5a"/><stop offset="1" stop-color="#0b0b10"/></linearGradient></defs><rect width="320" height="180" fill="url(#g)"/><text x="160" y="112" font-size="72" font-family="sans-serif" font-weight="700" fill="#a78bfa" text-anchor="middle">${ini}</text></svg>`);
  $$('.project img').forEach(img => img.addEventListener('error', () => { img.src = ph(img.dataset.ini || '?'); }, { once: true }));

  /* Íconos del toolkit: si no cargan, muestra la inicial */
  $$('.tool img').forEach(img => img.addEventListener('error', () => {
    const b = document.createElement('div');
    b.className = 'badge';
    b.textContent = $('span', img.parentNode).textContent[0];
    img.replaceWith(b);
  }, { once: true }));

  /* Foto de perfil */
  $('#foto').addEventListener('error', e => {
    e.target.src = 'data:image/svg+xml,' + encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200"><rect width="200" height="200" fill="#14141c"/><circle cx="100" cy="80" r="38" fill="#8b5cf6"/><path d="M25 200c0-55 33-85 75-85s75 30 75 85z" fill="#8b5cf6"/></svg>');
  }, { once: true });

  /* Imagen del hero: si falta, muestra una silueta */
  $('#hero-bg').addEventListener('error', e => {
    e.target.src = 'data:image/svg+xml,' + encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900"><defs><radialGradient id="g" cx=".75" cy=".4" r=".6"><stop offset="0" stop-color="#3b1d8a"/><stop offset="1" stop-color="#0b0b10"/></radialGradient></defs><rect width="1600" height="900" fill="url(#g)"/><circle cx="1180" cy="330" r="130" fill="#8b5cf6" opacity=".55"/><path d="M830 900c0-210 150-330 350-330s350 120 350 330z" fill="#8b5cf6" opacity=".55"/></svg>');
  }, { once: true });

  /* Copiar correo */
  $$('[data-copy]').forEach(btn => btn.addEventListener('click', async () => {
    try { await navigator.clipboard.writeText(btn.dataset.copy); btn.textContent = 'Copiado'; }
    catch (e) { btn.textContent = 'No se pudo copiar'; }
    setTimeout(() => (btn.textContent = 'Copiar'), 1800);
  }));

   /* Botón volver arriba */
  const toTop = $('#to-top');
  addEventListener('scroll', () => toTop.classList.toggle('show', scrollY > 500), { passive: true });
  toTop.addEventListener('click', () => scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }));

  $('#year').textContent = new Date().getFullYear();
})();