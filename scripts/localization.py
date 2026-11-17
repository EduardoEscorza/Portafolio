"""Selecciono únicamente las traducciones que utiliza cada página generada."""

import json
from html.parser import HTMLParser

TRANSLATABLE_ATTRIBUTES = {'aria-label', 'aria-roledescription', 'alt', 'content'}
# Incluyo esta etiqueta porque la agrego al abrir el menú móvil.
DYNAMIC_LABELS = {'Cerrar menú'}


class PageStrings(HTMLParser):
    """Recopilo los mismos textos y atributos que traduzco desde script.js."""

    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.values = set(DYNAMIC_LABELS)
        self.ignored_tag = None
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        if tag in {'script', 'style'}:
            self.ignored_tag = tag
        self.values.update(
            value for name, value in attrs
            if name in TRANSLATABLE_ATTRIBUTES and value
        )

    def handle_endtag(self, tag):
        if tag == self.ignored_tag:
            self.ignored_tag = None

    def handle_data(self, value):
        if not self.ignored_tag and value.strip():
            self.values.add(value.strip())


def page_translations(source, translations):
    """Inserto el JSON compacto de forma segura para evitar una descarga adicional en el navegador."""
    values = PageStrings(source).values
    selected = {key: value for key, value in translations.items() if key in values}
    return json.dumps(selected, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
