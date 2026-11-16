"""Generate and verify the static portfolio locally, without dependencies.

python scripts/build_site.py           Generate pages/mockups and validate them.
python scripts/build_site.py --check   Validate existing files without rewriting.
"""
import argparse
import sys
from pathlib import Path
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent

# Illustrative SVG mockups.
"""Illustrative SVG mockups with sample data; never actual project screenshots."""
from html import escape
INK='#203246'; DIM='#607286'; LINE='#dce4eb'; WHITE='#fff'; PANEL='#f1f5f8'
def rect(x,y,w,h,fill,rx=8,stroke=None):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"'+(f' stroke="{stroke}"' if stroke else '')+'/>'
def text(x,y,value,size=12,color=INK,weight=400):
 return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}">{escape(str(value))}</text>'
def line(x,y,w,color=LINE):return f'<path d="M{x} {y}h{w}" stroke="{color}"/>'
def pill(x,y,value,color='#287d85',width=72):return rect(x,y,width,20,color+'16',5)+text(x+8,y+14,value,9,color,600)
def sidebar(title,items,accent):
 s=rect(0,0,112,292,'#eaf0f5',0)+text(12,27,title,12,accent,700)
 for i,label in enumerate(items):
  y=52+i*34
  if i==0:s+=rect(8,y-17,96,28,accent,6)
  s+=text(17,y+1,label,10,WHITE if i==0 else DIM,600 if i==0 else 400)
 return s+text(14,275,'VISTA DE EJEMPLO',6,DIM)
def metric(x,y,label,value,accent,width=156):return rect(x,y,width,57,WHITE,8,LINE)+text(x+12,y+19,label,9,DIM)+text(x+12,y+43,value,21,accent,700)
def dashboard(slug,accent):
 if slug=='sigetu':
  s=sidebar('SIGETU',['Resumen','Estudiantes','Grupos','Materias'],accent)+text(130,28,'Gestión estudiantil',18,INK,700)+text(130,45,'Una vista de la información académica',9,DIM)
  for x,label,value in [(130,'Estudiantes','128'),(300,'Grupos','12'),(470,'Materias','8')]:s+=metric(x,59,label,value,accent)
  s+=rect(130,130,496,145,WHITE,8,LINE)+text(143,152,'Estudiantes · registros de ejemplo',11,INK,600)+rect(142,162,472,22,PANEL,4)+text(152,177,'Nombre',8,DIM,600)+text(360,177,'Grupo',8,DIM,600)+text(497,177,'Registro',8,DIM,600)
  for i in range(3):
   y=201+i*25;s+=text(153,y,f'Estudiante 0{i+1}',10)+text(360,y,f'Grupo {chr(65+i)}',9,DIM)+pill(497,y-14,'Académico',accent,91)+line(143,y+10,470)
  return s
 if slug=='sistema-de-ventas':
  s=sidebar('SELL / OUT',['Resumen','Ventas','Carga masiva','Reportes'],accent)+text(130,28,'Resumen de ventas',18,INK,700)+text(130,45,'Datos ilustrativos · periodo de ejemplo',9,DIM)
  for x,label,value in [(130,'Ventas','$24,580'),(300,'Registros','248'),(470,'Carga','Completa')]:s+=metric(x,59,label,value,accent)
  s+=rect(130,130,300,145,WHITE,8,LINE)+text(145,152,'Actividad del periodo',11,INK,600)
  for i,h in enumerate([34,58,45,73,63,85,99]):s+=rect(151+i*36,254-h,20,h,accent if i==6 else '#a4c4d6',4)
  return s+line(145,255,270)+rect(444,130,182,145,WHITE,8,LINE)+text(458,152,'Carga de información',11,INK,600)+text(458,178,'archivo_ejemplo.csv',9,DIM)+rect(458,191,150,6,accent,3)+pill(458,215,'Procesado',accent,92)+text(458,258,'Registros de muestra',8,DIM)
 if slug=='sistema-de-control-de-accesos':
  s=sidebar('ACCESOS',['Panel','Movimientos','Usuarios','Alertas'],accent)+text(130,28,'Control de accesos',18,INK,700)+text(130,45,'Identificación y seguimiento de movimientos',9,DIM)+rect(130,61,180,212,WHITE,8,LINE)+text(145,83,'Identificador QR',11,INK,600)
  for bx,by in [(151,99),(239,99),(151,187)]:s+=rect(bx,by,44,44,INK,2)+rect(bx+6,by+6,32,32,WHITE,0)+rect(bx+12,by+12,20,20,INK,0)
  # Non-encoded decorative pattern; never a functional authorization.
  for row in range(17):
   for col in range(17):
    if (col<6 and row<6) or (col>10 and row<6) or (col<6 and row>10):continue
    if (row*7+col*11+row*col)%5<2:s+=rect(151+col*7.7,99+row*7.7,6.8,6.8,INK,0)
  s+=pill(160,244,'Acceso permitido',accent,123)+rect(325,61,301,212,WHITE,8,LINE)+text(341,84,'Últimos movimientos',12,INK,600)
  for i,(label,tag) in enumerate([('Registro A','Entrada'),('Registro B','Salida'),('Registro C','Entrada'),('Registro D','Salida')]):
   y=116+i*41;s+=rect(340,y-15,22,22,accent+'18',6)+text(371,y,label,10)+pill(535,y-15,tag,accent,70)+line(341,y+16,266)
  return s
 if slug=='sistema-de-cargos-cruzados':
  s=sidebar('CARGOS',['Resumen','Movimientos','Establecimientos','Usuarios'],accent)+text(130,28,'Cargos entre establecimientos',18,INK,700)+text(130,45,'Integración hotelera · datos de ejemplo',9,DIM)+metric(130,59,'Origen','Unidad A',accent,240)+metric(386,59,'Destino','Unidad B',accent,240)+rect(130,130,496,145,WHITE,8,LINE)+text(145,153,'Movimientos ilustrativos',12,INK,600)+rect(143,166,470,22,PANEL,4)+text(153,181,'Referencia',8,DIM,600)+text(292,181,'Origen → Destino',8,DIM,600)+text(515,181,'Importe',8,DIM,600)
  for i,value in enumerate(['$1,200','$850','$420']):
   y=206+i*27;s+=text(153,y,f'Cargo 00{i+1}',10)+text(292,y,'Unidad A → Unidad B',9,DIM)+text(515,y,value,10,accent,600)+line(143,y+10,470)
  return s
 return ''
def store(accent,custom=False):
 s=rect(0,0,648,292,'#f5f3ed',0)+text(25,31,'TIENDA / A MEDIDA' if custom else 'ESTUDIO / TIENDA',15,INK,700)+text(380,30,'Colección     Catálogo     Carrito',10,DIM)+line(22,46,604,'#d8dfd9')+text(27,81,'Catálogo y compras en línea.' if custom else 'Una nueva forma de comprar.',22,INK,700)+text(28,102,'Colección ilustrativa · sin productos reales',10,DIM)+pill(492,69,'PHP · SQL · JS' if custom else 'Shopify',accent,125)
 for i,(color,label) in enumerate([('#a8b8a8','Colección 01'),('#bbab95','Colección 02'),('#9cb0ba','Colección 03')]):
  x=27+i*204;s+=rect(x,121,187,115,'#e5e8df',8)+f'<ellipse cx="{x+92}" cy="220" rx="48" ry="7" fill="#20324615"/>'+rect(x+64,155,59,62,color,12)+f'<path d="M{x+76} 155v-8a17 17 0 0 1 34 0v8" fill="none" stroke="{color}" stroke-width="7"/>'+text(x,255,label,11,INK,600)+text(x,273,'Producto de ejemplo',9,DIM)
 return s
def courses(accent):
 s=rect(0,0,648,292,'#f5f7fb',0)+text(24,29,'AULA / CURSOS',14,accent,700)+text(434,29,'Inicio    Cursos    Mi espacio',9,DIM)+line(23,44,600)+rect(22,59,604,93,'#dce7f0',10)+text(40,90,'Aprender, a tu ritmo.',24,INK,700)+text(41,111,'Un espacio para organizar cursos y contenidos.',10,DIM)+pill(42,121,'Explorar cursos',accent,119)+text(24,177,'Catálogo de cursos · vista ilustrativa',12,INK,600)
 for i,label in enumerate(['Desarrollo web','Bases de datos','Programación']):
  x=23+i*205;s+=rect(x,189,191,87,WHITE,8,LINE)+rect(x+10,199,37,37,accent+'16',8)+text(x+17,223,'</>',13,accent,700)+text(x+58,214,label,10,INK,600)+text(x+58,231,'Curso de ejemplo',8,DIM)+line(x+11,247,167)+text(x+12,265,'Ver contenido →',9,accent,600)
 return s
def mobile_ui(slug,accent):
 s=rect(0,0,212,374,'#f4f7fa',0)+text(13,20,'9:41',8,INK,600)+text(169,20,'● ▰',7)
 if slug=='gestor-de-gastos':
  s+=text(15,52,'Mis gastos',21,INK,700)+text(16,69,'Resumen mensual · ejemplo',8,DIM)+rect(13,82,186,74,accent,12)+text(25,102,'GASTOS DEL MES',8,'#dceef0',600)+text(24,130,'$2,450.00',26,WHITE,700)+text(25,145,'Datos de muestra',7,'#dceef0')+text(15,180,'Por categoría',11,INK,600)
  s+=f'<circle cx="53" cy="220" r="26" fill="none" stroke="#d9e4eb" stroke-width="10"/><circle cx="53" cy="220" r="26" fill="none" stroke="{accent}" stroke-width="10" stroke-dasharray="106 164" transform="rotate(-90 53 220)"/><circle cx="53" cy="220" r="26" fill="none" stroke="#c5a46f" stroke-width="10" stroke-dasharray="31 164" stroke-dashoffset="-109" transform="rotate(-90 53 220)"/>'
  for i,(label,color) in enumerate([('Alimentos',accent),('Transporte','#c5a46f'),('Otros','#9db4c5')]):s+=rect(98,197+i*20,6,6,color,2)+text(111,204+i*20,label,8,DIM)
  s+=text(15,268,'Movimientos de ejemplo',11,INK,600)
  for i,(label,value) in enumerate([('Alimentos','$180'),('Transporte','$80')]):
   y=292+i*29;s+=rect(13,y-15,186,25,WHITE,6)+rect(21,y-10,15,15,accent+'18',4)+text(43,y,label,9)+text(158,y,value,9,INK,600)
 else:
  s+=text(15,52,'Tu próximo traslado',16,INK,700)+text(15,69,'Ruta ilustrativa',8,DIM)+rect(12,83,188,163,'#e4ebe7',12)
  for x,y,w,h in [(22,93,40,29),(76,94,35,43),(126,92,62,26),(20,142,41,33),(72,150,48,22),(141,137,47,34),(22,190,51,43),(91,189,38,44),(145,187,40,46)]:s+=rect(x,y,w,h,'#ccd9d0',5)
  s+=f'<path d="M44 112h80v66h42v38" fill="none" stroke="{accent}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/><circle cx="44" cy="112" r="7" fill="{accent}" stroke="white" stroke-width="3"/><circle cx="166" cy="216" r="7" fill="{accent}" stroke="white" stroke-width="3"/>'+rect(13,258,186,72,WHITE,10,LINE)+text(25,279,'Origen → Destino',12,INK,600)+text(25,297,'Puntos de ejemplo',9,DIM)+pill(25,305,'Ver traslado',accent,111)
 return s+line(13,342,186)+text(30,360,'Inicio',8,accent,600)+text(91,360,'Actividad',8,DIM)+text(165,360,'Perfil',8,DIM)
def mockup(project):
 slug=project['slug'];colors={'sistema-de-cargos-cruzados':('#6c7293','#dce0e9'),'tienda-en-linea-a-medida':('#7a637d','#ded4e2'),'sigetu':('#416d8e','#d1dce9'),'sistema-de-ventas':('#356c85','#cddde7'),'sistema-de-control-de-accesos':('#287d72','#cfdfd8'),'migracion-de-tienda-a-shopify':('#53754a','#dce2d3'),'app-movil-de-traslados':('#3c7e89','#cddfe1'),'landing-page-y-gestion-de-cursos':('#626a9c','#d9ddeb'),'gestor-de-gastos':('#287d85','#d3e4e2')};accent,bg=colors.get(slug,('#287d85','#d3e0e5'))
 if project['device'] in ['mobile','backend']:
  device=rect(283,18,234,401,'#203246',31)+rect(292,27,216,383,'#f4f7fa',24)+f'<g clip-path="url(#screen)"><g transform="translate(294 30)">{mobile_ui(slug,accent)}</g></g>'+rect(369,29,62,9,'#203246',5)+rect(371,404,58,3,'#a9b9c9',2)
  deco=text(55,157,'ANDROID / MOBILE',9,accent,700)+text(55,182,'Gastos' if slug=='gestor-de-gastos' else 'Traslados',24,INK,700)+text(55,203,'Interfaz conceptual',10,DIM)
  if slug=='gestor-de-gastos':deco+=text(55,224,'Kotlin · Android Studio',9,DIM)
  if project['device']=='backend':deco+=text(55,224,'Mi participación: backend',9,DIM)
  clip='<rect x="294" y="30" width="212" height="374" rx="21"/>'
 else:
  content=store(accent,slug=='tienda-en-linea-a-medida') if slug in ['migracion-de-tienda-a-shopify','tienda-en-linea-a-medida'] else courses(accent) if slug=='landing-page-y-gestion-de-cursos' else dashboard(slug,accent)
  device=rect(63,27,674,346,'#203246',16)+rect(72,36,656,328,'#f4f7fa',9)+rect(76,40,648,24,'#d4dfe7',0)
  for x in [88,100,112]:device+=f'<circle cx="{x}" cy="52" r="3" fill="#8ba0b2"/>'
  device+=text(270,55,'workspace / '+project['title'],8,DIM)+f'<g clip-path="url(#screen)"><g transform="translate(76 64)">{content}</g></g><path d="M42 373h716l-30 27H72z" fill="#7690a5"/><path d="M336 373h128l-10 10h-108z" fill="#b8cad6"/>'
  clip='<rect x="76" y="64" width="648" height="292"/>';deco=''
 return f'<svg xmlns="http://www.w3.org/2000/svg" width="800" height="450" viewBox="0 0 800 450"><title>{escape(project["title"])} · mockup ilustrativo</title><desc>Interfaz conceptual con datos de ejemplo; no es una captura real ni una afirmación de funcionalidades implementadas.</desc><defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="{bg}"/><stop offset="1" stop-color="#a9bdcc"/></linearGradient><clipPath id="screen">{clip}</clipPath></defs><rect width="800" height="450" fill="url(#bg)"/><circle cx="710" cy="30" r="220" fill="{accent}" opacity=".05"/><g font-family="Arial,sans-serif">{deco}{device}{text(210,437,"MOCKUP ILUSTRATIVO · DATOS DE EJEMPLO",10,"#344c64",600)}</g></svg>'


# Static site generation.
def build_site():
    from html import escape as esc
    import json
    from datetime import date
    DATA = json.loads((ROOT / 'scripts' / 'content.json').read_text(encoding='utf-8'))
    PROJECTS = [p for p in DATA['projects'] if p['published']]

    def icon(name):
        paths = {'code': '<path d="m8 7-5 5 5 5m8-10 5 5-5 5m-3-14-2 18"/>', 'terminal': '<rect x="3" y="4" width="18" height="16" rx="3"/><path d="m7 9 3 3-3 3m6 0h4"/>', 'chip': '<rect x="7" y="7" width="10" height="10" rx="2"/><path d="M9 3v4m6-4v4M9 17v4m6-4v4M3 9h4m-4 6h4M17 9h4m-4 6h4"/>', 'cycle': '<path d="M4 12a8 8 0 0 1 14-5m2-3v4h-4m4 4a8 8 0 0 1-14 5m-2 3v-4h4"/>', 'data': '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 4 16 4 16 0V5M4 12c0 4 16 4 16 0"/>', 'api': '<rect x="8" y="8" width="8" height="8" rx="2"/><path d="M12 3v5m0 8v5M3 12h5m8 0h5M5 5l4 4m6 6 4 4M19 5l-4 4M9 15l-4 4"/>', 'chart': '<path d="M4 20V10m6 10V4m6 16v-8m6 8H2"/>', 'network': '<rect x="8" y="2" width="8" height="6" rx="1"/><rect x="2" y="16" width="7" height="5" rx="1"/><rect x="15" y="16" width="7" height="5" rx="1"/><path d="M12 8v4m-7 4v-4h14v4"/>', 'tools': '<path d="m14 6 4 4m-8 4-6 6-2-2 6-6m6 2 6 6 2-2-6-6M3 3l5 1 12 12M14 8a5 5 0 0 1 6-6l-3 3 2 2 3-3a5 5 0 0 1-6 6"/>'}
        return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + paths.get(name, paths['code']) + '</svg>'

    def external(url, text, cls=''):
        return f'<a class="{cls}" href="{esc(url, quote=True)}" target="_blank" rel="noopener">{text}</a>'

    def heading(title):
        return f'<div class="section-heading"><h2>{title}<span>.</span></h2></div>'

    def header(detail=False):
        base = '../index.html' if detail else ''
        items = [('inicio', 'Inicio'), ('proyectos', 'Proyectos'), ('hago', 'Cosas que hago'), ('toolkit', 'Herramientas'), ('contacto', 'Contacto')]
        links = ''.join((f'<a href="{base}#{slug}">{label}</a>' for slug, label in items))
        return f'''<a class="skip" href="#contenido">Saltar al contenido</a>\n<header class="nav"><div class="nav-inner container">\n<a class="logo" href="{base}#inicio"><span class="monogram">EE<span>.</span></span><span>{esc(DATA['name'])}<small>{esc(DATA['role'])}</small></span></a>\n<button class="burger" type="button" aria-label="Abrir menú" aria-controls="menu" aria-expanded="false"><span aria-hidden="true">☰</span></button>\n<nav id="menu" aria-label="Navegación principal">{links}<a class="btn nav-cta" href="{base}#contacto">Hablemos <span aria-hidden="true">↗</span></a></nav>\n</div></header>'''

    def footer(detail=False):
        base = '../index.html' if detail else ''
        return f'''<footer class="foot"><div class="container footer-inner"><a class="footer-name" href="{base}#inicio">EE. <span>{esc(DATA['name'])}</span></a><p>© <span id="year">{date.today().year}</span> · Desarrollo con propósito.</p><nav class="footer-links" aria-label="Enlaces del pie">{external(DATA['github'], 'GitHub ↗')}{external(DATA['linkedin'], 'LinkedIn ↗')}<a href="{base}#inicio">Volver arriba ↑</a></nav></div></footer>'''

    def shell(title, desc, body, detail=False):
        prefix = '../' if detail else ''
        return f'''<!doctype html>\n<!-- Generated by build_site.py -->\n<html lang="es">\n<head>\n  <meta charset="utf-8" />\n  <meta name="viewport" content="width=device-width, initial-scale=1" />\n  <meta name="description" content="{esc(desc, quote=True)}" />\n  <meta name="theme-color" content="#344C64" />\n  <title>{esc(title)} | {esc(DATA['name'])}</title>\n  <link rel="stylesheet" href="{prefix}styles.css" />\n  <script src="{prefix}script.js" defer></script>\n</head>\n<body>\n{header(detail)}\n<main id="contenido">{body}</main>\n{footer(detail)}\n</body>\n</html>\n'''

    def tool_item(tool, strip=False):
        return f'''<li class="tool"><img src="{tool['logo']}" alt="" width="32" height="32" loading="{('eager' if strip else 'lazy')}" /><span>{esc(tool['name'])}</span></li>'''
    SCENE = '<div class="hero-visual">\n<div class="scene-label"><span></span> WEB + MOBILE / WORKSPACE</div>\n<div class="scene-stage" tabindex="0" role="group" aria-label="Escena 3D de computadora y móvil. Arrastra con el ratón o usa las flechas para girar. Inicio restablece la vista." aria-describedby="scene-help">\n  <div class="scene-shadow" aria-hidden="true"></div>\n  <div class="scene-float" aria-hidden="true"><div class="scene-model">\n    <div class="desk"><div class="desk-edge"></div></div>\n    <div class="monitor">\n      <div class="monitor-back"></div>\n      <div class="monitor-screen">\n        <div class="editor-bar"><i></i><i></i><i></i><span>portfolio / workspace</span></div>\n        <div class="editor"><div class="editor-sidebar"><b>EXPLORER</b><span>⌄ src</span><span>index.html</span><span>styles.css</span><span>app.js</span></div><div class="editor-code"><span class="code-muted">// De la idea al código</span><b>&lt;software&gt;</b><span>const idea = {</span><span class="code-indent">web: true,</span><span class="code-indent">mobile: true</span><span>};</span><b>&lt;/software&gt;</b></div></div>\n        <div class="editor-status">main* <span>UTF-8 · JavaScript</span></div>\n      </div>\n      <div class="monitor-neck"></div><div class="monitor-foot"></div>\n    </div>\n    <div class="keyboard"><span></span></div><div class="mouse"></div>\n    <div class="phone"><div class="phone-camera"></div><div class="phone-screen"><div class="phone-top">9:41 <span>● ▰</span></div><span class="phone-greeting">MI ESPACIO</span><strong>Todo en orden.</strong><div class="phone-card"><span>Actividad</span><b>Esta semana</b><div class="phone-chart"><i></i><i></i><i></i><i></i><i></i></div></div><div class="phone-row"><i></i><span>Proyecto web<small>En desarrollo</small></span></div><div class="phone-row"><i></i><span>Aplicación móvil<small>En desarrollo</small></span></div><div class="phone-navigation">⌂ <span>＋</span> ☰</div></div><div class="phone-home"></div></div>\n  </div></div>\n</div>\n<p id="scene-help" class="scene-hint">Arrastra para explorar · ← → para girar · Inicio para restablecer</p>\n</div>'
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
    body = f'''\n<section id="inicio" class="hero container" aria-labelledby="hero-title"><div class="hero-main"><div class="hero-in"><p class="hero-greeting">Hola, soy</p><h1 id="hero-title">{DATA['name']}</h1><p class="hero-role">{DATA['role']}</p><p class="lead">Transformo ideas en sistemas útiles.<br /> Desarrollo web, servicios y aplicaciones conectadas.</p><div class="cta"><a class="btn" href="#proyectos">Ver proyectos <span aria-hidden="true">↗</span></a><a class="btn alt" href="{esc(DATA['cv'], quote=True)}" target="_blank" rel="noopener">Descargar CV <span aria-hidden="true">↓</span></a></div><p class="hero-note"><span aria-hidden="true">&lt;/&gt;</span> Código claro. Soluciones con propósito.</p></div>{SCENE}</div><div class="tool-strip"><p>HERRAMIENTAS QUE UTILIZO</p><ul>{strip}</ul></div></section>\n<section id="proyectos" class="sec container">{heading('Proyectos seleccionados')}<p class="section-note">Participación, soluciones y tecnologías. Las imágenes son mockups ilustrativos con datos de ejemplo, no capturas reales.</p><div class="grid">{''.join((project_card(p, i) for i, p in enumerate(PROJECTS, 1)))}</div></section>\n<section id="hago" class="sec container">{heading('Cosas que hago')}<div class="services-grid">{service_cards}</div>{cert_block}</section>\n<section id="toolkit" class="sec container">{heading('Herramientas y tecnologías')}<p class="section-note">Herramientas que utilizo para desarrollar y colaborar, agrupadas por su función.</p><div class="groups">{groups}</div></section>\n{contact}'''
    (ROOT / 'index.html').write_text(shell('Full Stack Developer', 'Portafolio de Eduardo Escorza. Desarrollo web, APIs y aplicaciones. Proyectos, herramientas y forma de trabajo.', body), encoding='utf-8')
    pages = ROOT / 'proyectos'
    pages.mkdir(exist_ok=True)
    published_slugs = {p['slug'] for p in PROJECTS}
    for previous in pages.glob('*.html'):
        if previous.stem not in published_slugs and '<!-- Generated by build_site.py -->' in previous.read_text(encoding='utf-8'):
            previous.unlink()

    def paragraphs(values):
        return ''.join((f'<p>{esc(value)}</p>' for value in values))

    def project_technologies(project):
        return ''.join((f'<div class="project-tech-group"><h3>{esc(group)}</h3><ul class="chips">' + ''.join((f'<li>{esc(item)}</li>' for item in items)) + '</ul></div>' for group, items in project['technology_groups'].items()))
    for p in PROJECTS:
        tech = ''.join((f'<li>{esc(t)}</li>' for t in p['technologies']))
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

# HTML, local resource and editorial checks.
def verify_site():
    from html.parser import HTMLParser
    from urllib.parse import urlsplit, unquote
    import json
    import xml.etree.ElementTree as ET
    VOID = set('area base br col embed hr img input link meta param source track wbr'.split())

    class Page(HTMLParser):

        def __init__(self, path):
            super().__init__(convert_charrefs=True)
            self.path = path
            self.stack = []
            self.ids = set()
            self.refs = []
            self.h1 = 0

        def handle_starttag(self, tag, attrs):
            a = dict(attrs)
            assert not any((k.startswith('on') for k in a)), f'Inline event: {self.path}'
            if tag == 'h1':
                self.h1 += 1
            if tag == 'img':
                assert 'alt' in a and 'width' in a and ('height' in a), f'Image attributes: {self.path}'
            if tag == 'a' and a.get('target') == '_blank':
                assert 'noopener' in a.get('rel', ''), f'Unsafe new tab: {self.path}'
            if 'id' in a:
                assert a['id'] not in self.ids, f'Duplicate id: {self.path}'
                self.ids.add(a['id'])
            for key in ['href', 'src']:
                if key in a:
                    assert a[key] and (not a[key].startswith(('javascript:', 'http:'))), f'Unsafe URL: {self.path}'
                    self.refs.append(a[key])
            if tag not in VOID:
                self.stack.append(tag)

        def handle_startendtag(self, tag, attrs):
            self.handle_starttag(tag, attrs)
            if tag not in VOID:
                self.stack.pop()

        def handle_endtag(self, tag):
            assert self.stack and self.stack[-1] == tag, f'Unbalanced markup: {self.path}: {tag}'
            self.stack.pop()
    pages = {}
    for path in [ROOT / 'index.html', *sorted((ROOT / 'proyectos').glob('*.html'))]:
        page = Page(path)
        source = path.read_text(encoding='utf-8-sig')
        assert '�' not in source, f'Encoding: {path}'
        page.feed(source)
        assert not page.stack and page.h1 == 1, f'HTML structure: {path}'
        pages[path] = page
    refs = 0
    for path, page in pages.items():
        for ref in page.refs:
            u = urlsplit(ref)
            if u.scheme or u.netloc:
                continue
            target = (path.parent / unquote(u.path)).resolve() if u.path else path
            assert target.exists(), f'Missing local file: {path}: {ref}'
            # GitHub Pages uses case-sensitive asset paths.
            parent = ROOT
            for part in target.relative_to(ROOT).parts:
                assert part in {entry.name for entry in parent.iterdir()}, f'Incorrect filename case: {ref}'
                parent = parent / part
            if u.fragment and target in pages:
                assert u.fragment in pages[target].ids, f'Missing anchor: {ref}'
            refs += 1
    for svg in (ROOT / 'img').rglob('*.svg'):
        for e in ET.parse(svg).iter():
            assert e.tag.split('}')[-1] not in ['script', 'foreignObject'], f'Active SVG: {svg}'
            assert not any((k.lower().startswith('on') for k in e.attrib)), f'Active SVG attribute: {svg}'
    data = json.loads((ROOT / 'scripts' / 'content.json').read_text(encoding='utf-8'))
    published = [p for p in data['projects'] if p['published']]
    assert len(pages) == len(published) + 1
    for p in data['projects']:
        if not p['published']:
            assert not (ROOT / 'proyectos' / (p['slug'] + '.html')).exists(), 'Draft has a public page'
        else:
            assert all((p.get(k) for k in ['role', 'description', 'participation', 'features', 'technology_groups', 'technologies']))
    index = (ROOT / 'index.html').read_text(encoding='utf-8')
    hero = index[index.index('<section id="inicio"'):index.index('<section id="proyectos"')]
    assert 'portrait' not in hero and 'img1.png' not in hero
    assert '<p class="hero-greeting">Hola, soy</p>' in hero
    assert '<h1 id="hero-title">Eduardo Escorza</h1>' in hero
    assert '<p class="hero-role">Full Stack Developer</p>' in hero
    assert index.count('class="scene-stage"') == 1
    assert index.index('id="hago"') < index.index('id="certificados"') < index.index('id="toolkit"')
    assert len([c for c in data['certificates'] if c['published']]) == 6
    assert len(data['tools']) == 33
    assert any((p['slug'] == 'gestor-de-gastos' and p['technologies'][:2] == ['Kotlin', 'Android Studio'] for p in published))
    assert '01 / DEL CONCEPTO' not in index and '02 / CÓMO' not in index and ('03 / HERRAMIENTAS' not in index)
    mockups = [(ROOT / 'img' / 'proyectos' / (p['slug'] + '.svg')).read_text(encoding='utf-8') for p in published]
    assert len(set(mockups)) == len(published)
    assert all(('MOCKUP ILUSTRATIVO' in m and 'DATOS DE EJEMPLO' in m for m in mockups))
    assert len(published) == 9
    assert not (ROOT / 'proyectos' / 'expediente-clinico-digital.html').exists()
    assert 'expediente-clinico-digital' not in index
    all_public = '\n'.join((path.read_text(encoding='utf-8') for path in pages))
    assert 'Notas de integración' not in all_public and 'Instrucciones generales para Codex' not in all_public
    assert '70%' not in all_public
    backend = next((p for p in published if p['device'] == 'backend'))
    assert backend['technologies'] == ['Node.js', 'TypeScript', 'Moleculer', 'MySQL', 'Procedimientos almacenados']
    assert len([p for p in published if p.get('result')]) == 2
    for p in published:
        html = (ROOT / 'proyectos' / (p['slug'] + '.html')).read_text(encoding='utf-8')
        from html import escape
        assert escape(p['role']) in html
        assert all((escape(paragraph) in html for paragraph in p['description'] + p['participation']))
        assert ('Resultado destacado' in html) == bool(p.get('result'))
        assert ('<h2>Estado' in html) == bool(p.get('status'))
        assert 'loading="lazy"' in html
        assert 'href="../index.html#proyectos"' in html and 'href="../index.html#contacto"' in html
    print(f'PASS: {len(pages)} HTML pages, {refs} local references, all SVGs, project fields, draft exclusion, exact hero text and certificates within services.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Genera y verifica el portafolio estático sin dependencias.')
    parser.add_argument('--check', action='store_true', help='Verifica los archivos actuales sin regenerarlos.')
    args = parser.parse_args()
    if not args.check:
        build_site()
    verify_site()
