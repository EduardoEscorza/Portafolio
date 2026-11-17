"""Creo mockups SVG ilustrativos con datos de ejemplo, sin utilizar capturas reales.

Uso un patrón QR decorativo que no contiene ninguna autorización de acceso.
"""

from html import escape
INK = '#203246'
DIM = '#607286'
LINE = '#dce4eb'
WHITE = '#fff'
PANEL = '#f1f5f8'

def rect(x, y, w, h, fill, rx=8, stroke=None):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"' + (f' stroke="{stroke}"' if stroke else '') + '/>'

def text(x, y, value, size=12, color=INK, weight=400):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}">{escape(str(value))}</text>'

def line(x, y, w, color=LINE):
    return f'<path d="M{x} {y}h{w}" stroke="{color}"/>'

def pill(x, y, value, color='#287d85', width=72):
    return rect(x, y, width, 20, color + '16', 5) + text(x + 8, y + 14, value, 9, color, 600)

def sidebar(title, items, accent):
    s = rect(0, 0, 112, 292, '#eaf0f5', 0) + text(12, 27, title, 12, accent, 700)
    for i, label in enumerate(items):
        y = 52 + i * 34
        if i == 0:
            s += rect(8, y - 17, 96, 28, accent, 6)
        s += text(17, y + 1, label, 10, WHITE if i == 0 else DIM, 600 if i == 0 else 400)
    return s + text(14, 275, 'VISTA DE EJEMPLO', 6, DIM)

def metric(x, y, label, value, accent, width=156):
    return rect(x, y, width, 57, WHITE, 8, LINE) + text(x + 12, y + 19, label, 9, DIM) + text(x + 12, y + 43, value, 21, accent, 700)

def dashboard(slug, accent):
    if slug == 'expediente-clinico':
        s = sidebar('CLÍNICO', ['Expedientes', 'Usuarios', 'Perfiles', 'Catálogos'], accent) + text(130, 28, 'Expediente clínico digital', 18, INK, 700) + text(130, 45, 'Vista conceptual · sin información clínica', 9, DIM)
        s += rect(130, 62, 300, 212, WHITE, 8, LINE) + rect(144, 76, 34, 34, accent + '16', 8)
        s += f'<path d="M153 87h7l3 3h8v12h-18z" fill="none" stroke="{accent}" stroke-width="1.5" stroke-linejoin="round"/>'
        s += text(189, 89, 'Ficha de referencia', 12, INK, 600) + text(189, 105, 'Estructura ilustrativa', 8, DIM) + line(145, 122, 270)
        for i, label in enumerate(['Identificación', 'Información general', 'Documentación']):
            y = 145 + i * 40
            s += text(146, y, label, 9, DIM) + rect(146, y + 8, 210 if i == 1 else 252, 7, '#e5edf1', 3)
        s += text(146, 258, 'Sin datos personales ni clínicos', 8, DIM)
        s += rect(444, 62, 182, 212, WHITE, 8, LINE) + text(458, 86, 'Administración', 12, INK, 600)
        for i, label in enumerate(['Usuarios', 'Perfiles y permisos', 'Catálogos']):
            y = 107 + i * 46
            s += rect(457, y, 156, 36, PANEL, 6) + rect(466, y + 10, 16, 16, accent + '18', 4) + text(489, y + 23, label, 9, INK, 600)
        return s + text(458, 258, 'INTERFAZ DE EJEMPLO', 7, DIM, 600)
    if slug == 'sigetu':
        s = sidebar('SIGETU', ['Resumen', 'Estudiantes', 'Grupos', 'Materias'], accent) + text(130, 28, 'Gestión estudiantil', 18, INK, 700) + text(130, 45, 'Una vista de la información académica', 9, DIM)
        for x, label, value in [(130, 'Estudiantes', '128'), (300, 'Grupos', '12'), (470, 'Materias', '8')]:
            s += metric(x, 59, label, value, accent)
        s += rect(130, 130, 496, 145, WHITE, 8, LINE) + text(143, 152, 'Estudiantes · registros de ejemplo', 11, INK, 600) + rect(142, 162, 472, 22, PANEL, 4) + text(152, 177, 'Nombre', 8, DIM, 600) + text(360, 177, 'Grupo', 8, DIM, 600) + text(497, 177, 'Registro', 8, DIM, 600)
        for i in range(3):
            y = 201 + i * 25
            s += text(153, y, f'Estudiante 0{i + 1}', 10) + text(360, y, f'Grupo {chr(65 + i)}', 9, DIM) + pill(497, y - 14, 'Académico', accent, 91) + line(143, y + 10, 470)
        return s
    if slug == 'sistema-de-ventas':
        s = sidebar('SELL / OUT', ['Resumen', 'Ventas', 'Carga masiva', 'Reportes'], accent) + text(130, 28, 'Resumen de ventas', 18, INK, 700) + text(130, 45, 'Datos ilustrativos · periodo de ejemplo', 9, DIM)
        for x, label, value in [(130, 'Ventas', '$24,580'), (300, 'Registros', '248'), (470, 'Carga', 'Completa')]:
            s += metric(x, 59, label, value, accent)
        s += rect(130, 130, 300, 145, WHITE, 8, LINE) + text(145, 152, 'Actividad del periodo', 11, INK, 600)
        for i, h in enumerate([34, 58, 45, 73, 63, 85, 99]):
            s += rect(151 + i * 36, 254 - h, 20, h, accent if i == 6 else '#a4c4d6', 4)
        return s + line(145, 255, 270) + rect(444, 130, 182, 145, WHITE, 8, LINE) + text(458, 152, 'Carga de información', 11, INK, 600) + text(458, 178, 'archivo_ejemplo.csv', 9, DIM) + rect(458, 191, 150, 6, accent, 3) + pill(458, 215, 'Procesado', accent, 92) + text(458, 258, 'Registros de muestra', 8, DIM)
    if slug == 'sistema-de-control-de-accesos':
        s = sidebar('ACCESOS', ['Panel', 'Movimientos', 'Usuarios', 'Alertas'], accent) + text(130, 28, 'Control de accesos', 18, INK, 700) + text(130, 45, 'Identificación y seguimiento de movimientos', 9, DIM) + rect(130, 61, 180, 212, WHITE, 8, LINE) + text(145, 83, 'Identificador QR', 11, INK, 600)
        for bx, by in [(151, 99), (239, 99), (151, 187)]:
            s += rect(bx, by, 44, 44, INK, 2) + rect(bx + 6, by + 6, 32, 32, WHITE, 0) + rect(bx + 12, by + 12, 20, 20, INK, 0)
        for row in range(17):
            for col in range(17):
                if col < 6 and row < 6 or (col > 10 and row < 6) or (col < 6 and row > 10):
                    continue
                if (row * 7 + col * 11 + row * col) % 5 < 2:
                    s += rect(151 + col * 7.7, 99 + row * 7.7, 6.8, 6.8, INK, 0)
        s += pill(160, 244, 'Acceso permitido', accent, 123) + rect(325, 61, 301, 212, WHITE, 8, LINE) + text(341, 84, 'Últimos movimientos', 12, INK, 600)
        for i, (label, tag) in enumerate([('Registro A', 'Entrada'), ('Registro B', 'Salida'), ('Registro C', 'Entrada'), ('Registro D', 'Salida')]):
            y = 116 + i * 41
            s += rect(340, y - 15, 22, 22, accent + '18', 6) + text(371, y, label, 10) + pill(535, y - 15, tag, accent, 70) + line(341, y + 16, 266)
        return s
    if slug == 'sistema-de-cargos-cruzados':
        s = sidebar('CARGOS', ['Resumen', 'Movimientos', 'Establecimientos', 'Usuarios'], accent) + text(130, 28, 'Cargos entre establecimientos', 18, INK, 700) + text(130, 45, 'Integración hotelera · datos de ejemplo', 9, DIM) + metric(130, 59, 'Origen', 'Unidad A', accent, 240) + metric(386, 59, 'Destino', 'Unidad B', accent, 240) + rect(130, 130, 496, 145, WHITE, 8, LINE) + text(145, 153, 'Movimientos ilustrativos', 12, INK, 600) + rect(143, 166, 470, 22, PANEL, 4) + text(153, 181, 'Referencia', 8, DIM, 600) + text(292, 181, 'Origen → Destino', 8, DIM, 600) + text(515, 181, 'Importe', 8, DIM, 600)
        for i, value in enumerate(['$1,200', '$850', '$420']):
            y = 206 + i * 27
            s += text(153, y, f'Cargo 00{i + 1}', 10) + text(292, y, 'Unidad A → Unidad B', 9, DIM) + text(515, y, value, 10, accent, 600) + line(143, y + 10, 470)
        return s
    return ''

def store(accent, custom=False):
    s = rect(0, 0, 648, 292, '#f5f3ed', 0) + text(25, 31, 'TIENDA / A MEDIDA' if custom else 'ESTUDIO / TIENDA', 15, INK, 700) + text(380, 30, 'Colección     Catálogo     Carrito', 10, DIM) + line(22, 46, 604, '#d8dfd9') + text(27, 81, 'Catálogo y compras en línea.' if custom else 'Una nueva forma de comprar.', 22, INK, 700) + text(28, 102, 'Colección ilustrativa · sin productos reales', 10, DIM) + pill(492, 69, 'PHP · SQL · JS' if custom else 'Shopify', accent, 125)
    for i, (color, label) in enumerate([('#a8b8a8', 'Colección 01'), ('#bbab95', 'Colección 02'), ('#9cb0ba', 'Colección 03')]):
        x = 27 + i * 204
        s += rect(x, 121, 187, 115, '#e5e8df', 8) + f'<ellipse cx="{x + 92}" cy="220" rx="48" ry="7" fill="#20324615"/>' + rect(x + 64, 155, 59, 62, color, 12) + f'<path d="M{x + 76} 155v-8a17 17 0 0 1 34 0v8" fill="none" stroke="{color}" stroke-width="7"/>' + text(x, 255, label, 11, INK, 600) + text(x, 273, 'Producto de ejemplo', 9, DIM)
    return s

def courses(accent):
    s = rect(0, 0, 648, 292, '#f5f7fb', 0) + text(24, 29, 'AULA / CURSOS', 14, accent, 700) + text(434, 29, 'Inicio    Cursos    Mi espacio', 9, DIM) + line(23, 44, 600) + rect(22, 59, 604, 93, '#dce7f0', 10) + text(40, 90, 'Aprender, a tu ritmo.', 24, INK, 700) + text(41, 111, 'Un espacio para organizar cursos y contenidos.', 10, DIM) + pill(42, 121, 'Explorar cursos', accent, 119) + text(24, 177, 'Catálogo de cursos · vista ilustrativa', 12, INK, 600)
    for i, label in enumerate(['Desarrollo web', 'Bases de datos', 'Programación']):
        x = 23 + i * 205
        s += rect(x, 189, 191, 87, WHITE, 8, LINE) + rect(x + 10, 199, 37, 37, accent + '16', 8) + text(x + 17, 223, '</>', 13, accent, 700) + text(x + 58, 214, label, 10, INK, 600) + text(x + 58, 231, 'Curso de ejemplo', 8, DIM) + line(x + 11, 247, 167) + text(x + 12, 265, 'Ver contenido →', 9, accent, 600)
    return s

def mobile_ui(slug, accent):
    s = rect(0, 0, 212, 374, '#f4f7fa', 0) + text(13, 20, '9:41', 8, INK, 600) + text(169, 20, '● ▰', 7)
    if slug == 'gestor-de-gastos':
        s += text(15, 52, 'Mis gastos', 21, INK, 700) + text(16, 69, 'Resumen mensual · ejemplo', 8, DIM) + rect(13, 82, 186, 74, accent, 12) + text(25, 102, 'GASTOS DEL MES', 8, '#dceef0', 600) + text(24, 130, '$2,450.00', 26, WHITE, 700) + text(25, 145, 'Datos de muestra', 7, '#dceef0') + text(15, 180, 'Por categoría', 11, INK, 600)
        s += f'<circle cx="53" cy="220" r="26" fill="none" stroke="#d9e4eb" stroke-width="10"/><circle cx="53" cy="220" r="26" fill="none" stroke="{accent}" stroke-width="10" stroke-dasharray="106 164" transform="rotate(-90 53 220)"/><circle cx="53" cy="220" r="26" fill="none" stroke="#c5a46f" stroke-width="10" stroke-dasharray="31 164" stroke-dashoffset="-109" transform="rotate(-90 53 220)"/>'
        for i, (label, color) in enumerate([('Alimentos', accent), ('Transporte', '#c5a46f'), ('Otros', '#9db4c5')]):
            s += rect(98, 197 + i * 20, 6, 6, color, 2) + text(111, 204 + i * 20, label, 8, DIM)
        s += text(15, 268, 'Movimientos de ejemplo', 11, INK, 600)
        for i, (label, value) in enumerate([('Alimentos', '$180'), ('Transporte', '$80')]):
            y = 292 + i * 29
            s += rect(13, y - 15, 186, 25, WHITE, 6) + rect(21, y - 10, 15, 15, accent + '18', 4) + text(43, y, label, 9) + text(158, y, value, 9, INK, 600)
    else:
        s += text(15, 52, 'Tu próximo traslado', 16, INK, 700) + text(15, 69, 'Ruta ilustrativa', 8, DIM) + rect(12, 83, 188, 163, '#e4ebe7', 12)
        for x, y, w, h in [(22, 93, 40, 29), (76, 94, 35, 43), (126, 92, 62, 26), (20, 142, 41, 33), (72, 150, 48, 22), (141, 137, 47, 34), (22, 190, 51, 43), (91, 189, 38, 44), (145, 187, 40, 46)]:
            s += rect(x, y, w, h, '#ccd9d0', 5)
        s += f'<path d="M44 112h80v66h42v38" fill="none" stroke="{accent}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/><circle cx="44" cy="112" r="7" fill="{accent}" stroke="white" stroke-width="3"/><circle cx="166" cy="216" r="7" fill="{accent}" stroke="white" stroke-width="3"/>' + rect(13, 258, 186, 72, WHITE, 10, LINE) + text(25, 279, 'Origen → Destino', 12, INK, 600) + text(25, 297, 'Puntos de ejemplo', 9, DIM) + pill(25, 305, 'Ver traslado', accent, 111)
    return s + line(13, 342, 186) + text(30, 360, 'Inicio', 8, accent, 600) + text(91, 360, 'Actividad', 8, DIM) + text(165, 360, 'Perfil', 8, DIM)

def mockup(project):
    slug = project['slug']
    colors = {'expediente-clinico': ('#387e83', '#d3e5e3'), 'sistema-de-cargos-cruzados': ('#6c7293', '#dce0e9'), 'tienda-en-linea-a-medida': ('#7a637d', '#ded4e2'), 'sigetu': ('#416d8e', '#d1dce9'), 'sistema-de-ventas': ('#356c85', '#cddde7'), 'sistema-de-control-de-accesos': ('#287d72', '#cfdfd8'), 'migracion-de-tienda-a-shopify': ('#53754a', '#dce2d3'), 'app-movil-de-traslados': ('#3c7e89', '#cddfe1'), 'landing-page-y-gestion-de-cursos': ('#626a9c', '#d9ddeb'), 'gestor-de-gastos': ('#287d85', '#d3e4e2')}
    accent, bg = colors.get(slug, ('#287d85', '#d3e0e5'))
    if project['device'] in ['mobile', 'backend']:
        device = rect(283, 18, 234, 401, '#203246', 31) + rect(292, 27, 216, 383, '#f4f7fa', 24) + f'<g clip-path="url(#screen)"><g transform="translate(294 30)">{mobile_ui(slug, accent)}</g></g>' + rect(369, 29, 62, 9, '#203246', 5) + rect(371, 404, 58, 3, '#a9b9c9', 2)
        deco = text(55, 157, 'ANDROID / MOBILE', 9, accent, 700) + text(55, 182, 'Gastos' if slug == 'gestor-de-gastos' else 'Traslados', 24, INK, 700) + text(55, 203, 'Interfaz conceptual', 10, DIM)
        if slug == 'gestor-de-gastos':
            deco += text(55, 224, 'Kotlin · Android Studio', 9, DIM)
        if project['device'] == 'backend':
            deco += text(55, 224, 'Mi participación: backend', 9, DIM)
        clip = '<rect x="294" y="30" width="212" height="374" rx="21"/>'
    else:
        content = store(accent, slug == 'tienda-en-linea-a-medida') if slug in ['migracion-de-tienda-a-shopify', 'tienda-en-linea-a-medida'] else courses(accent) if slug == 'landing-page-y-gestion-de-cursos' else dashboard(slug, accent)
        device = rect(63, 27, 674, 346, '#203246', 16) + rect(72, 36, 656, 328, '#f4f7fa', 9) + rect(76, 40, 648, 24, '#d4dfe7', 0)
        for x in [88, 100, 112]:
            device += f'<circle cx="{x}" cy="52" r="3" fill="#8ba0b2"/>'
        device += text(270, 55, 'workspace / ' + project['title'], 8, DIM) + f'<g clip-path="url(#screen)"><g transform="translate(76 64)">{content}</g></g><path d="M42 373h716l-30 27H72z" fill="#7690a5"/><path d="M336 373h128l-10 10h-108z" fill="#b8cad6"/>'
        clip = '<rect x="76" y="64" width="648" height="292"/>'
        deco = ''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="450" viewBox="0 0 800 450"><title>{escape(project['title'])} · mockup ilustrativo</title><desc>Interfaz conceptual con datos de ejemplo; no es una captura real ni una afirmación de funcionalidades implementadas.</desc><defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="{bg}"/><stop offset="1" stop-color="#a9bdcc"/></linearGradient><clipPath id="screen">{clip}</clipPath></defs><rect width="800" height="450" fill="url(#bg)"/><circle cx="710" cy="30" r="220" fill="{accent}" opacity=".05"/><g font-family="Arial,sans-serif">{deco}{device}{text(210, 437, 'MOCKUP ILUSTRATIVO · DATOS DE EJEMPLO', 10, '#344c64', 600)}</g></svg>'''
