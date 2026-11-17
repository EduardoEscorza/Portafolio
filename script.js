(() => {
  'use strict';
  function initLanguage() {
    // Conservo los nodos originales para mantener los enlaces, iconos y eventos al cambiar de idioma.
    const buttons = [...document.querySelectorAll('[data-language]')];
    const burger = document.querySelector('.burger');
    const translations = JSON.parse(document.querySelector('#translations')?.textContent || '{}');
    const textNodes = [];
    const walker = document.createTreeWalker(document.documentElement, NodeFilter.SHOW_TEXT, {
      acceptNode: node => node.parentElement?.closest('script, style') ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT
    });
    while (walker.nextNode()) {
      const node = walker.currentNode;
      if (translations[node.textContent.trim()]) textNodes.push([node, node.textContent]);
    }
    const attributes = [];
    document.querySelectorAll('[aria-label], [aria-roledescription], img[alt], meta[name="description"]').forEach(element => {
      for (const name of ['aria-label', 'aria-roledescription', 'alt', 'content']) {
        const value = element.getAttribute(name);
        if (translations[value]) attributes.push([element, name, value]);
      }
    });
    const translate = value => document.documentElement.lang === 'en' ? (translations[value] || value) : value;
    const setLanguage = language => {
      const lang = language === 'en' ? 'en' : 'es';
      document.documentElement.lang = lang;
      for (const [node, original] of textNodes) {
        node.textContent = original.replace(original.trim(), lang === 'en' ? translations[original.trim()] : original.trim());
      }
      for (const [element, name, original] of attributes) element.setAttribute(name, translate(original));
      buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.language === lang)));
      burger?.setAttribute('aria-label', translate(burger.getAttribute('aria-expanded') === 'true' ? 'Cerrar menú' : 'Abrir menú'));
      try { localStorage.setItem('portfolio-language', lang); } catch { /* Continúo aunque el navegador no permita guardar la preferencia. */ }
    };
    let preferred = 'es';
    try { preferred = localStorage.getItem('portfolio-language') || preferred; } catch { /* Uso español si no puedo consultar la preferencia guardada. */ }
    const requested = new URLSearchParams(location.search).get('lang');
    setLanguage(['es', 'en'].includes(requested) ? requested : preferred);
    buttons.forEach(button => button.addEventListener('click', () => {
      setLanguage(button.dataset.language);
      // Actualizo el idioma de la URL cuando ya incluye una selección explícita.
      const url = new URL(location.href);
      if (url.searchParams.has('lang')) {
        url.searchParams.set('lang', button.dataset.language);
        history.replaceState(null, '', url);
      }
    }));
    return translate;
  }

  function initNavigation(translate) {
    const burger = document.querySelector('.burger');
    const menu = document.querySelector('#menu');
    const closeMenu = () => {
      menu?.classList.remove('open');
      burger?.setAttribute('aria-expanded', 'false');
      burger?.setAttribute('aria-label', translate('Abrir menú'));
    };
    burger?.addEventListener('click', () => {
      const open = menu.classList.toggle('open');
      burger.setAttribute('aria-expanded', String(open));
      burger.setAttribute('aria-label', translate(open ? 'Cerrar menú' : 'Abrir menú'));
    });
    menu?.addEventListener('click', event => {
      if (event.target.closest('a')) closeMenu();
    });
    document.addEventListener('click', event => {
      if (!event.target.closest('.nav')) closeMenu();
    });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && menu?.classList.contains('open')) {
        closeMenu();
        burger.focus();
      }
    });
    matchMedia('(min-width: 1051px)').addEventListener('change', closeMenu);
    const year = document.querySelector('#year');
    if (year) year.textContent = new Date().getFullYear();

  }

  function initScene(reduced) {
    // Construyo la escena con CSS 3D, sin depender de WebGL ni de un ciclo de renderizado continuo.
    const stage = document.querySelector('.scene-stage');
    const model = stage?.querySelector('.scene-model');
    if (stage && model) {
      const clamp = (value, low, high) => Math.max(low, Math.min(high, value));
      let drag = null;
      let frame = null;
      const render = (yaw = -15, pitch = -8) => {
        cancelAnimationFrame(frame);
        frame = requestAnimationFrame(() => {
          model.style.setProperty('--yaw', `${clamp(yaw, -33, 3)}deg`);
          model.style.setProperty('--pitch', `${clamp(pitch, -17, 1)}deg`);
        });
      };
      const reset = () => render();
      stage.addEventListener('pointerdown', event => {
        // Permito desplazar la página con el dedo y reservo el giro para el ratón o el lápiz.
        if (event.pointerType === 'touch' || !event.isPrimary || event.button !== 0 || reduced.matches) return;
        drag = { id: event.pointerId, x: event.clientX, y: event.clientY };
        stage.setPointerCapture(event.pointerId);
        stage.classList.add('dragging');
        stage.focus({ preventScroll: true });
      });
      stage.addEventListener('pointermove', event => {
        if (reduced.matches || event.pointerType === 'touch') return;
        if (drag && event.pointerId === drag.id) {
          render(-15 + (event.clientX - drag.x) * .12, -8 - (event.clientY - drag.y) * .06);
        } else if (event.pointerType === 'mouse' && matchMedia('(hover: hover)').matches) {
          const box = stage.getBoundingClientRect();
          render(-15 + ((event.clientX - box.left) / box.width - .5) * 5, -8 - ((event.clientY - box.top) / box.height - .5) * 3);
        }
      });
      const release = event => {
        if (!drag || event.pointerId !== drag.id) return;
        drag = null;
        stage.classList.remove('dragging');
        if (stage.hasPointerCapture(event.pointerId)) stage.releasePointerCapture(event.pointerId);
        reset();
      };
      ['pointerup', 'pointercancel', 'lostpointercapture'].forEach(name => stage.addEventListener(name, release));
      stage.addEventListener('pointerleave', () => { if (!drag) reset(); });
      stage.addEventListener('blur', reset);
      stage.addEventListener('keydown', event => {
        if (!['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Home'].includes(event.key)) return;
        event.preventDefault();
        if (event.key === 'Home') return reset();
        if (reduced.matches) return;
        const yaw = parseFloat(model.style.getPropertyValue('--yaw')) || -15;
        const pitch = parseFloat(model.style.getPropertyValue('--pitch')) || -8;
        render(yaw + (event.key === 'ArrowLeft' ? -4 : event.key === 'ArrowRight' ? 4 : 0), pitch + (event.key === 'ArrowUp' ? -2 : event.key === 'ArrowDown' ? 2 : 0));
      });
      reduced.addEventListener('change', reset);
      if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver(entries => {
          stage.classList.toggle('scene-visible', entries[0].isIntersecting);
        });
        observer.observe(stage);
      }
    }

  }

  function initCertificates(reduced) {
    const track = document.querySelector('#certificate-track');
    const controls = [...document.querySelectorAll('.carousel-controls .nav-btn')];
    if (track) {
      const update = () => {
        const max = track.scrollWidth - track.clientWidth;
        controls.forEach(button => {
          button.disabled = Number(button.dataset.dir) < 0 ? track.scrollLeft <= 2 : track.scrollLeft >= max - 2;
        });
      };
      const move = direction => {
        const card = track.querySelector('.cert');
        const gap = parseFloat(getComputedStyle(track).gap) || 0;
        track.scrollBy({ left: direction * ((card?.getBoundingClientRect().width || 280) + gap), behavior: reduced.matches ? 'instant' : 'smooth' });
      };
      controls.forEach(button => button.addEventListener('click', () => move(Number(button.dataset.dir))));
      track.addEventListener('keydown', event => {
        if (event.target !== track || !['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
        event.preventDefault();
        if (event.key === 'Home' || event.key === 'End') track.scrollTo({ left: event.key === 'Home' ? 0 : track.scrollWidth, behavior: reduced.matches ? 'instant' : 'smooth' });
        else move(event.key === 'ArrowLeft' ? -1 : 1);
      });
      track.addEventListener('scroll', update, { passive: true });
      if ('ResizeObserver' in window) new ResizeObserver(update).observe(track);
      else window.addEventListener('resize', update);
      update();
    }
  }

  function initReveals(reduced) {
    // Animo la entrada una sola vez y mantengo el contenido visible si se desactivan las animaciones o JavaScript.
    if (!reduced.matches && 'IntersectionObserver' in window) {
      const reveal = new IntersectionObserver(entries => {
        entries.forEach(entry => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add('reveal-enter');
          reveal.unobserve(entry.target);
        });
      }, { threshold: .08 });
      document.querySelectorAll('.project, .mini, .tool-group, .detail-panel, .contact-photo, .contact-copy').forEach(el => reveal.observe(el));
      reduced.addEventListener('change', event => {
        if (event.matches) {
          reveal.disconnect();
          document.querySelectorAll('.reveal-enter').forEach(el => el.classList.remove('reveal-enter'));
        }
      });
    }
  }

  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const translate = initLanguage();
  initNavigation(translate);
  initScene(reduced);
  initCertificates(reduced);
  initReveals(reduced);
})();
