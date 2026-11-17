"""Genero el portafolio estático desde content.json y después valido el resultado.

python scripts/build_site.py          Genero el HTML y los SVG, y después los compruebo.
python scripts/build_site.py --check  Compruebo los archivos existentes sin reescribirlos.
"""

import argparse
import json
import sys
from datetime import date
from html import escape as esc
from pathlib import Path

sys.dont_write_bytecode = True

from check_site import verify_site
from localization import page_translations
from mockups import mockup

ROOT = Path(__file__).resolve().parent.parent

# Genero las páginas estáticas a partir de los datos del portafolio.
def build_site():
    DATA = json.loads((ROOT / 'scripts' / 'content.json').read_text(encoding='utf-8'))
    translations = json.loads((ROOT / 'scripts/translations.json').read_text(encoding='utf-8'))
    PROJECTS = [p for p in DATA['projects'] if p['published']]

    def icon(name):
        paths = {'code': '<path d="m8 7-5 5 5 5m8-10 5 5-5 5m-3-14-2 18"/>', 'terminal': '<rect x="3" y="4" width="18" height="16" rx="3"/><path d="m7 9 3 3-3 3m6 0h4"/>', 'chip': '<rect x="7" y="7" width="10" height="10" rx="2"/><path d="M9 3v4m6-4v4M9 17v4m6-4v4M3 9h4m-4 6h4M17 9h4m-4 6h4"/>', 'cycle': '<path d="M4 12a8 8 0 0 1 14-5m2-3v4h-4m4 4a8 8 0 0 1-14 5m-2 3v-4h4"/>', 'data': '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 4 16 4 16 0V5M4 12c0 4 16 4 16 0"/>', 'api': '<rect x="8" y="8" width="8" height="8" rx="2"/><path d="M12 3v5m0 8v5M3 12h5m8 0h5M5 5l4 4m6 6 4 4M19 5l-4 4M9 15l-4 4"/>', 'chart': '<path d="M4 20V10m6 10V4m6 16v-8m6 8H2"/>', 'network': '<rect x="8" y="2" width="8" height="6" rx="1"/><rect x="2" y="16" width="7" height="5" rx="1"/><rect x="15" y="16" width="7" height="5" rx="1"/><path d="M12 8v4m-7 4v-4h14v4"/>', 'tools': '<path d="m14 6 4 4m-8 4-6 6-2-2 6-6m6 2 6 6 2-2-6-6M3 3l5 1 12 12M14 8a5 5 0 0 1 6-6l-3 3 2 2 3-3a5 5 0 0 1-6 6"/>'}
        return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + paths.get(name, paths['code']) + '</svg>'

    def external(url, text, cls=''):
        class_attribute = f' class="{cls}"' if cls else ''
        return f'<a{class_attribute} href="{esc(url, quote=True)}" target="_blank" rel="noopener">{text}</a>'

    def heading(title):
        return f'<div class="section-heading"><h2>{title}<span>.</span></h2></div>'

    def header(detail=False):
        base = '../index.html' if detail else ''
        items = [('inicio', 'Inicio'), ('proyectos', 'Proyectos'), ('hago', 'Cosas que hago'), ('toolkit', 'Herramientas'), ('contacto', 'Contacto')]
        links = ''.join((f'<a href="{base}#{slug}">{label}</a>' for slug, label in items))
        return f'''<a class="skip" href="#contenido">Saltar al contenido</a>\n<header class="nav"><div class="nav-inner container">\n<a class="logo" href="{base}#inicio"><span class="monogram">EE<span>.</span></span><span>{esc(DATA['name'])}<small>{esc(DATA['role'])}</small></span></a>\n<button class="burger" type="button" aria-label="Abrir menú" aria-controls="menu" aria-expanded="false"><span aria-hidden="true">☰</span></button>\n<nav id="menu" aria-label="Navegación principal">{links}<a class="btn nav-cta" href="{base}#contacto">Hablemos <span aria-hidden="true">↗</span></a></nav><div class="language-switch" role="group" aria-label="Idioma"><button type="button" data-language="es" aria-pressed="true" lang="es" aria-label="Español"><img src="{('../' if detail else '')}img/flags/mx.svg" alt="" width="20" height="14" aria-hidden="true" />ES</button><button type="button" data-language="en" aria-pressed="false" lang="en" aria-label="English"><img src="{('../' if detail else '')}img/flags/us.svg" alt="" width="20" height="14" aria-hidden="true" />EN</button></div>\n</div></header>'''

    def footer(detail=False):
        base = '../index.html' if detail else ''
        return f'''<footer class="foot"><div class="container footer-inner"><a class="footer-name" href="{base}#inicio">EE. <span>{esc(DATA['name'])}</span></a><p>© <span id="year">{date.today().year}</span> · Desarrollo con propósito.</p><nav class="footer-links" aria-label="Enlaces del pie">{external(DATA['github'], 'GitHub ↗')}{external(DATA['linkedin'], 'LinkedIn ↗')}<a href="{base}#inicio">Volver arriba ↑</a></nav></div></footer>'''

    def shell(title, desc, body, detail=False):
        prefix = '../' if detail else ''
        document = f'''<!doctype html>\n<!-- Genero este archivo con build_site.py. -->\n<html lang="es">\n<head>\n  <meta charset="utf-8" />\n  <meta name="viewport" content="width=device-width, initial-scale=1" />\n  <meta name="description" content="{esc(desc, quote=True)}" />\n  <meta name="theme-color" content="#344C64" />\n  <title>{esc(title)} | {esc(DATA['name'])}</title>\n  <link rel="stylesheet" href="{prefix}styles.css" />\n  <script type="application/json" id="translations">__PAGE_TRANSLATIONS__</script>\n  <script src="{prefix}script.js" defer></script>\n</head>\n<body>\n{header(detail)}\n<main id="contenido">{body}</main>\n{footer(detail)}\n</body>\n</html>\n'''
        return document.replace('__PAGE_TRANSLATIONS__', page_translations(document, translations))

    def tool_item(tool, strip=False):
        return f'''<li class="tool"><img src="{tool['logo']}" alt="" width="32" height="32" loading="{('eager' if strip else 'lazy')}" /><span>{esc(tool['name'])}</span></li>'''
    SCENE = (ROOT / 'scripts/templates/scene.html').read_text(encoding='utf-8').rstrip()
    mockups = ROOT / 'img' / 'proyectos'
    mockups.mkdir(parents=True, exist_ok=True)
    for p in PROJECTS:
        (mockups / (p['slug'] + '.svg')).write_text(mockup(p), encoding='utf-8')

    def project_image(p, prefix=''):
        image = p['screenshots'][0] if p['screenshots'] else f"img/proyectos/{p['slug']}.svg"
        alt = f"Captura de {p['title']}" if p['screenshots'] else f"Mockup ilustrativo de {p['title']}; interfaz conceptual con datos de ejemplo"
        return f'<img src="{prefix}{esc(image, quote=True)}" alt="{esc(alt, quote=True)}" width="800" height="450" loading="lazy" />'

    def project_card(p, index):
        chips = ''.join((f'<li>{esc(t)}</li>' for t in p['technologies'][:3]))
        return f"""<article class="project"><a class="project-image" href="proyectos/{p['slug']}.html" tabindex="-1" aria-hidden="true">{project_image(p)}<span class="project-index">{index:02}</span></a><div class="project-body"><p class="eyebrow project-category">{esc(p['category'])}</p><h3>{esc(p['title'])}</h3><p class="project-role">{esc(p['role'])}</p><p class="project-description">{esc(p['summary'])}</p><ul class="chips">{chips}</ul><a class="text-link" href="proyectos/{p['slug']}.html" aria-label="Ver proyecto: {esc(p['title'], quote=True)}">Ver proyecto <span aria-hidden="true">↗</span></a></div></article>"""
    services = [('code', 'Desarrollo web', 'Interfaces claras y aplicaciones adaptables a cada pantalla.'), ('api', 'APIs e integraciones', 'Servicios para conectar sistemas, usuarios e información.'), ('data', 'Bases de datos', 'Modelado, consultas y procedimientos almacenados.'), ('tools', 'Mantenimiento y mejoras', 'Optimización, soporte y evolución de sistemas existentes.')]
    service_cards = ''.join((f'<article class="mini"><span class="service-icon">{icon(i)}</span><h3>{t}</h3><p>{d}</p></article>' for i, t, d in services))
    certs = [c for c in DATA['certificates'] if c['published'] and (ROOT / c['file']).exists()]
    cert_cards = ''
    for c in certs:
        date_html = f'''<time datetime="{c.get('date') or c['year']}">{c['year']}</time>''' if c.get('year') else ''
        issuer_html = f"<p>{esc(c['issuer'])}</p>" if c.get('issuer') else ''
        description_html = f"<p>{esc(c['description'])}</p>" if c.get('description') else ''
        links = external(c['file'], 'Consultar PDF ↗', 'text-link')
        if c.get('verify'):
            links += external(c['verify'], 'Verificar ↗', 'text-link')
        cert_cards += f"""<article class="cert"><span class="service-icon">{icon(c['icon'])}</span><h4>{esc(c['title'])}</h4>{issuer_html}{date_html}{description_html}<div class="cert-links">{links}</div></article>"""
    cert_block = f'<div id="certificados" class="certificates" aria-labelledby="cert-title"><div class="cert-heading"><div><h3 id="cert-title">Certificados</h3></div><div class="carousel-controls"><button class="nav-btn" type="button" data-dir="-1" aria-label="Certificado anterior" aria-controls="certificate-track">←</button><button class="nav-btn" type="button" data-dir="1" aria-label="Certificado siguiente" aria-controls="certificate-track">→</button></div></div><div id="certificate-track" class="track" tabindex="0" role="region" aria-roledescription="carrusel" aria-label="Certificados. Usa las flechas izquierda y derecha para desplazarte.">{cert_cards}</div><p class="carousel-help">Desliza o usa las flechas para explorar. Sin reproducción automática.</p></div>' if certs else ''
    groups = ''
    for group in dict.fromkeys((t['group'] for t in DATA['tools'])):
        groups += f'<article class="tool-group"><h3>{group}</h3><ul class="tools">' + ''.join((tool_item(t) for t in DATA['tools'] if t['group'] == group)) + '</ul></article>'
    groups += f"""<article class="tool-group work-method"><h3>Forma de trabajo</h3><div class="method-icon">{icon('cycle')}</div><h4>Scrum</h4><p>Marco de trabajo ágil para organizar tareas en iteraciones, revisar avances y mejorar de forma continua.</p><div class="method-tags"><span>Planeación</span><span>Comunicación</span><span>Mejora continua</span></div></article>"""
    featured_by_name = {t['name']: t for t in DATA['tools'] if t['featured']}
    strip = ''.join((tool_item(featured_by_name[n], True) for n in ['Shopify', 'Android Studio', 'Visual Studio Code', 'Claude Code', 'Codex', 'AWS']))
    contact = f'''<section id="contacto" class="sec container contact-section" aria-labelledby="contact-title"><figure class="contact-photo"><img id="foto" src="{DATA['photo']}" alt="Retrato de Eduardo Escorza" width="450" height="600" loading="lazy" /></figure><div class="contact-copy"><h2 id="contact-title">¿Tienes un proyecto en mente?</h2><p>Me interesa construir soluciones útiles y colaborar en nuevos retos. Cuéntame qué necesitas y conversemos sobre el siguiente paso.</p><div class="contact-links"><a href="mailto:{DATA['email']}"><span>Correo</span>{DATA['email']} <b aria-hidden="true">↗</b></a>{external(DATA['github'], '<span>GitHub</span>EduardoEscorza <b aria-hidden="true">↗</b>')}{external(DATA['linkedin'], '<span>LinkedIn</span>Eduardo Escorza <b aria-hidden="true">↗</b>')}</div></div></section>'''
    body = f'''\n<section id="inicio" class="hero container" aria-labelledby="hero-title"><div class="hero-main"><div class="hero-in"><p class="hero-greeting">Hola, soy</p><h1 id="hero-title">{DATA['name']}</h1><p class="hero-role">{DATA['role']}</p><p class="lead">Transformo ideas en sistemas útiles.<br /> Desarrollo web, servicios y aplicaciones conectadas.</p><div class="cta"><a class="btn" href="#proyectos">Ver proyectos <span aria-hidden="true">↗</span></a><a class="btn alt" href="{esc(DATA['cv'], quote=True)}" target="_blank" rel="noopener">Descargar CV <span aria-hidden="true">↓</span></a></div><p class="hero-note"><span aria-hidden="true">&lt;/&gt;</span> Código claro. Soluciones con propósito.</p></div>{SCENE}</div><div class="tool-strip"><ul>{strip}</ul></div></section>\n<section id="proyectos" class="sec container">{heading('Proyectos seleccionados')}<p class="section-note">Participación, soluciones y tecnologías. Las imágenes son mockups ilustrativos con datos de ejemplo, no capturas reales.</p><div class="grid">{''.join((project_card(p, i) for i, p in enumerate(PROJECTS, 1)))}</div></section>\n<section id="hago" class="sec container">{heading('Cosas que hago')}<div class="services-grid">{service_cards}</div>{cert_block}</section>\n<section id="toolkit" class="sec container">{heading('Herramientas y tecnologías')}<p class="section-note">Herramientas que utilizo para desarrollar y colaborar, agrupadas por su función.</p><div class="groups">{groups}</div></section>\n{contact}'''
    (ROOT / 'index.html').write_text(shell('Full Stack Developer', 'Portafolio de Eduardo Escorza. Desarrollo web, APIs y aplicaciones. Proyectos, herramientas y forma de trabajo.', body), encoding='utf-8')
    pages = ROOT / 'proyectos'
    pages.mkdir(exist_ok=True)
    published_slugs = {p['slug'] for p in PROJECTS}
    for previous in pages.glob('*.html'):
        if previous.stem not in published_slugs and '<!-- Genero este archivo con build_site.py. -->' in previous.read_text(encoding='utf-8'):
            previous.unlink()

    def paragraphs(values):
        return ''.join((f'<p>{esc(value)}</p>' for value in values))

    def project_technologies(project):
        return ''.join((f'<div class="project-tech-group"><h3>{esc(group)}</h3><ul class="chips">' + ''.join((f'<li>{esc(item)}</li>' for item in items)) + '</ul></div>' for group, items in project['technology_groups'].items()))
    for p in PROJECTS:
        features = ''.join((f'<li>{esc(t)}</li>' for t in p['features']))
        extras = ''.join((f"<figure>{project_image(dict(p, screenshots=[im]), '../')}</figure>" for im in p['screenshots'][1:]))
        extra_section = f'<section class="sec container"><h2>Más capturas</h2><div class="screenshots">{extras}</div></section>' if extras else ''
        links = ''
        for key, label in [('demo', 'Ver demostración ↗'), ('repository', 'Ver repositorio ↗')]:
            if p.get(key) and p[key].startswith('https://'):
                links += external(p[key], label, 'btn')
        status_panel = ''
        if p.get('status') or links:
            status = f"<p>{esc(p['status'])}</p>" if p.get('status') else ''
            status_panel = f"""<article class="detail-panel"><span class="service-icon">{icon('cycle')}</span><h2>Estado{(' y enlaces' if links else '')}</h2>{status}<div class="cta">{links}</div></article>"""
        result_panel = f"""<article class="detail-panel project-result"><span class="service-icon">{icon('chart')}</span><h2>Resultado destacado</h2><p>{esc(p['result'])}</p></article>""" if p.get('result') else ''
        picture_note = 'Captura del proyecto.' if p['screenshots'] else 'Mockup ilustrativo del producto · Mi participación fue exclusivamente en el backend.' if p['device'] == 'backend' else 'Mockup ilustrativo · Interfaz conceptual con datos de ejemplo, no es una captura real.'
        detail = f"""<section id="inicio" class="sec container detail-hero"><a class="text-link" href="../index.html#proyectos">← Volver a proyectos</a><p class="eyebrow">{esc(p['category'])}</p><h1>{esc(p['title'])}</h1><p class="project-role">{esc(p['role'])}</p><p class="detail-lead">{esc(p['summary'])}</p></section><section class="container detail-overview"><figure class="project-figure">{project_image(p, '../')}<figcaption>{picture_note}</figcaption></figure><div class="detail-copy"><article><h2>Descripción del proyecto</h2>{paragraphs(p['description'])}</article></div></section><section class="sec container detail-content"><article class="detail-panel"><span class="service-icon">{icon('code')}</span><h2>Mi participación</h2>{paragraphs(p['participation'])}</article><article class="detail-panel"><span class="service-icon">{icon('api')}</span><h2>{esc(p['features_title'])}</h2><ul class="feature-list">{features}</ul></article><article class="detail-panel"><span class="service-icon">{icon('terminal')}</span><h2>Tecnologías y recursos</h2>{project_technologies(p)}</article>{result_panel}{status_panel}</section>{extra_section}<div class="container detail-back"><a class="text-link" href="../index.html#proyectos">← Regresar al listado de proyectos</a><a class="text-link" href="../index.html#contacto">Hablemos de tu proyecto ↗</a></div>"""
        (pages / (p['slug'] + '.html')).write_text(shell(p['title'], p['summary'], detail, True), encoding='utf-8')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Genera y verifica el portafolio estático sin dependencias.')
    parser.add_argument('--check', action='store_true', help='Verifica los archivos actuales sin regenerarlos.')
    args = parser.parse_args()
    if not args.check:
        build_site()
    verify_site(ROOT)
