#!/usr/bin/env python3
"""
Build script para generar presentaciones standalone
Genera un index.html en la carpeta de la presentación con todo lo necesario
"""

import os
import sys
import yaml
import re
from pathlib import Path


def parse_yaml_frontmatter(content):
    """Extrae y parsea el frontmatter YAML del markdown"""
    if not content.startswith('---'):
        return {}, content

    # Buscar el segundo ---
    end_index = content.find('---', 3)
    if end_index == -1:
        return {}, content

    yaml_content = content[3:end_index].strip()
    markdown_content = content[end_index + 3:].strip()

    try:
        metadata = yaml.safe_load(yaml_content)
        return metadata or {}, markdown_content
    except yaml.YAMLError as e:
        print(f"⚠️  Error parsing YAML: {e}")
        return {}, markdown_content


def process_markdown_to_slides(markdown_content):
    """Convierte el markdown en estructura de slides"""
    # Dividir por <!-- SLIDE -->
    slides = []
    slide_blocks = re.split(r'<!--\s*SLIDE\s*-->', markdown_content)

    for block in slide_blocks:
        block = block.strip()
        if not block:
            continue

        # Dividir por <!-- SUBSLIDE -->
        subslides = re.split(r'<!--\s*SUBSLIDE\s*-->', block)
        slide_group = []

        for subslide in subslides:
            subslide = subslide.strip()
            if not subslide:
                continue

            # Extraer marcadores especiales
            is_inverted = '<!-- INVERTED -->' in subslide
            subslide = subslide.replace('<!-- INVERTED -->', '').strip()

            bg_match = re.search(r'<!--\s*BACKGROUND:\s*([^\s]+)\s*-->', subslide)
            background_image = bg_match.group(1) if bg_match else None
            if background_image:
                subslide = re.sub(r'<!--\s*BACKGROUND:\s*[^\s]+\s*-->', '', subslide).strip()

            # Separar contenido y notas
            parts = re.split(r'<!--\s*NOTES\s*-->', subslide, 1)
            content = parts[0].strip()
            notes = parts[1].strip() if len(parts) > 1 else ''

            slide_group.append({
                'content': content,
                'notes': notes,
                'is_inverted': is_inverted,
                'background_image': background_image
            })

        if slide_group:
            slides.append(slide_group)

    return slides


def escape_html(text):
    """Escapa caracteres HTML"""
    return (text.replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&#39;'))


def generate_html(presentation_name, metadata, slides):
    """Genera el HTML completo de la presentación"""

    # Colores por defecto
    colors = metadata.get('colors', {})
    bg_color = colors.get('background', '#FFFFFF')
    text_color = colors.get('text-color', '#000000')
    heading_color = colors.get('heading-color', colors.get('main-color', '#DF006E'))
    heading2_color = colors.get('heading2-color', '#0078D7')
    heading3_color = colors.get('heading3-color', '#000035')

    # Fuentes
    fonts = metadata.get('fonts', {})
    main_font = fonts.get('main-font', 'Lato, sans-serif')
    heading_font = fonts.get('heading-font', 'Lato, sans-serif')
    heading_fontsize = fonts.get('heading-fontsize', '3rem')

    # Configuración
    font_size = metadata.get('fontSize', '30px')
    theme = metadata.get('theme', 'white')
    transition = metadata.get('transition', 'slide')
    transition_speed = metadata.get('transitionSpeed', 'default')

    # Generar slides HTML
    slides_html = []
    for slide_group in slides:
        if len(slide_group) == 1:
            # Slide simple
            slides_html.append(generate_slide_html(slide_group[0], metadata))
        else:
            # Slide con subslides
            inner_slides = '\n'.join([generate_slide_html(s, metadata) for s in slide_group])
            slides_html.append(f'<section>\n{inner_slides}\n</section>')

    slides_content = '\n'.join(slides_html)

    # Template HTML
    html = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{presentation_name}</title>
    <link href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../reveal.js/dist/reveal.css">
    <link rel="stylesheet" href="../reveal.js/dist/theme/{theme}.css">
    <style>
        :root {{
            --heading1-color: {heading_color};
            --heading2-color: {heading2_color};
            --heading3-color: {heading3_color};
            --heading-fontsize: {heading_fontsize};
        }}
        body {{
            font-family: {main_font};
            font-size: {font_size};
            background-color: {bg_color};
        }}
        .reveal {{
            font-family: {main_font};
        }}
        .reveal h1 {{
            color: {heading_color} !important;
            font-size: {heading_fontsize} !important;
            font-family: {heading_font};
        }}
        .reveal h2 {{
            color: {heading2_color} !important;
            font-size: calc({heading_fontsize} * 0.85) !important;
            font-family: {heading_font};
        }}
        .reveal h3 {{
            color: {heading3_color} !important;
            font-size: calc({heading_fontsize} * 0.7) !important;
            font-family: {heading_font};
        }}
        .reveal .slides,
        .reveal .slides section {{
            background: transparent !important;
            color: {text_color};
        }}

        /* Columnas */
        .columns {{
            display: flex;
            gap: 2rem;
            margin: 1.5rem 0;
        }}
        .columns > div {{
            flex: 1 1 0;
            min-width: 0;
            padding: 0 1rem;
        }}

        /* Grid */
        .grid-container {{
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
            margin: 1.5rem 0;
        }}
        .grid-row {{
            display: flex;
            gap: 2rem;
        }}
        .grid-cell {{
            flex: 1 1 0;
            min-width: 0;
            padding: 1rem;
            background: #f5f5f5;
            border-radius: 0.5rem;
            border: 1px solid #e0e0e0;
        }}

        /* Slides invertidas */
        .reveal .slides section[data-inverted="true"] h1,
        .reveal .slides section[data-inverted="true"] h2,
        .reveal .slides section[data-inverted="true"] h3,
        .reveal .slides section[data-inverted="true"] p,
        .reveal .slides section[data-inverted="true"] li,
        .reveal .slides section[data-inverted="true"] strong {{
            color: {bg_color} !important;
        }}
    </style>
</head>
<body>
    <div class="reveal">
        <div class="slides">
{slides_content}
        </div>
    </div>

    <script src="../reveal.js/dist/reveal.js"></script>
    <script src="../reveal.js/plugin/markdown/markdown.js"></script>
    <script src="../reveal.js/plugin/notes/notes.js"></script>
    <script src="../reveal.js/marked.min.js"></script>
    <script>
        Reveal.initialize({{
            hash: true,
            slideNumber: true,
            controls: true,
            progress: true,
            center: true,
            transition: '{transition}',
            transitionSpeed: '{transition_speed}',
            plugins: [ RevealMarkdown, RevealNotes ],
            markdown: {{
                smartypants: true,
                gfm: true
            }}
        }});

        // Procesar markdown en columnas y grids
        document.querySelectorAll('.columns > div').forEach(cell => {{
            if (cell.hasAttribute('data-markdown')) {{
                const md = decodeURIComponent(cell.getAttribute('data-markdown'));
                cell.innerHTML = marked.parse(md);
            }}
        }});

        document.querySelectorAll('.grid-cell').forEach(cell => {{
            if (cell.hasAttribute('data-markdown')) {{
                const md = decodeURIComponent(cell.getAttribute('data-markdown'));
                cell.innerHTML = marked.parse(md);
            }}
        }});
    </script>
</body>
</html>'''

    return html


def generate_slide_html(slide_data, metadata):
    """Genera el HTML de una slide individual"""
    content = slide_data['content']
    notes = slide_data['notes']
    is_inverted = slide_data['is_inverted']
    background_image = slide_data['background_image']

    # Colores para invertido
    colors = metadata.get('colors', {})
    bg_color_inverted = colors.get('text-color', '#000000')
    text_color_inverted = colors.get('background', '#FFFFFF')

    # Procesar columnas
    content = process_columns(content)
    # Procesar grids
    content = process_grids(content)
    # Procesar markdown
    content = process_markdown(content)

    # Atributos de la sección
    attrs = []
    if is_inverted:
        attrs.append('data-inverted="true"')
        attrs.append(f'data-background-color="{bg_color_inverted}"')
    if background_image:
        attrs.append(f'data-background-image="{background_image}"')
        attrs.append('data-background-size="cover"')
        attrs.append('data-background-position="center"')

    attrs_str = ' '.join(attrs)

    # Generar HTML
    html = f'<section {attrs_str}>\n{content}\n'

    if notes:
        notes_html = f'<aside class="notes">{process_markdown(notes)}</aside>'
        html += notes_html

    html += '</section>'

    return html


def process_columns(content):
    """Procesa el formato de columnas"""
    def replace_columns(match):
        columns_content = match.group(1)
        cols = [c.strip() for c in columns_content.split('$COL$') if c.strip()]
        cols_html = '\n'.join([f'<div data-markdown="{escape_attr(col)}"></div>' for col in cols])
        return f'<div class="columns">\n{cols_html}\n</div>'

    return re.sub(r'\$COLUMNS\$(.*?)\$END\$', replace_columns, content, flags=re.DOTALL)


def process_grids(content):
    """Procesa el formato de grids"""
    def replace_grid(match):
        grid_content = match.group(1)
        rows = [r.strip() for r in grid_content.split('$ROW$') if r.strip()]
        rows_html = []
        for row in rows:
            cells = [c.strip() for c in row.split('$CELL$') if c.strip()]
            cells_html = '\n'.join([f'<div class="grid-cell" data-markdown="{escape_attr(cell)}"></div>' for cell in cells])
            rows_html.append(f'<div class="grid-row">\n{cells_html}\n</div>')
        return f'<div class="grid-container">\n' + '\n'.join(rows_html) + '\n</div>'

    return re.sub(r'\$GRID\$(.*?)\$END\$', replace_grid, content, flags=re.DOTALL)


def escape_attr(text):
    """Escapa texto para atributos HTML (URL encode)"""
    import urllib.parse
    return urllib.parse.quote(text)


def process_markdown(content):
    """Procesa markdown básico (simulado, en el navegador usa marked.js)"""
    # Por ahora retornamos el contenido tal cual
    # El procesamiento real lo hace marked.js en el navegador
    return content


def build_presentation(presentation_name):
    """Construye una presentación standalone"""
    presentation_path = Path(presentation_name)

    if not presentation_path.exists():
        print(f"❌ Error: La carpeta '{presentation_name}' no existe")
        return False

    contenidos_path = presentation_path / 'contenidos.md'
    if not contenidos_path.exists():
        print(f"❌ Error: No se encontró '{contenidos_path}'")
        return False

    print(f"📦 Construyendo presentación: {presentation_name}")

    # Leer contenido
    with open(contenidos_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parsear
    metadata, markdown_content = parse_yaml_frontmatter(content)
    slides = process_markdown_to_slides(markdown_content)

    print(f"   ✓ Metadata parseada")
    print(f"   ✓ {len(slides)} slides procesadas")

    # Generar HTML
    html = generate_html(presentation_name, metadata, slides)

    # Guardar
    output_path = presentation_path / 'index.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"   ✓ Generado: {output_path}")
    print(f"✅ Build completado exitosamente")
    print(f"\n🌐 Abre: {output_path}")

    return True


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 build.py <nombre-presentacion>")
        print("\nEjemplo:")
        print("  python3 build.py equipazgo")
        sys.exit(1)

    presentation_name = sys.argv[1]
    success = build_presentation(presentation_name)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
